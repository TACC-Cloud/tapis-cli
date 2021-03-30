import docker as dockerpy
import os
import urllib.parse

from tapis_cli import settings
from tapis_cli.settings.helpers import parse_boolean
from tapis_cli.utils import (seconds, milliseconds, print_stderr)
from tapis_cli.commands.taccapis.v2.actors.manage.create import ActorsCreate
from tapis_cli.clients.services.mixins import (WorkingDirectoryArg, IniLoader,
                                               DockerPy)

from ..manage import ActorsCreate
from ..mixins import ActorIdentifier
from ..formatters import ActorsFormatManyUnlimited
from .. import API_NAME, SERVICE_VERSION

from . import actorid, rcfile

ENVS_FILE = 'secrets.json'

__all__ = ['ActorsDeploy']


class WorkflowFailed(Exception):
    pass


# class UploadAppTemplate(UploadJSONTemplate):
#     default = 'app.json'
#     optional = True

# TODO - Identify and implement other run-time overrides as they make sense


class ActorsDeploy(ActorsFormatManyUnlimited, DockerPy, WorkingDirectoryArg,
                   IniLoader):

    HELP_STRING = 'Deploy an Actor from a project directory'
    LEGACY_COMMMAND_STRING = 'abaco deploy'

    config = {}
    document = None
    results = []
    messages = []
    passed_vals = {}

    # Workflow control flags
    build = True
    pull = True
    push = True
    create = True
    grant = True

    def get_parser(self, prog_name):
        parser = super(ActorsDeploy, self).get_parser(prog_name)
        # Mixins
        parser = IniLoader.extend_parser(self, parser)
        # parser = WorkingDirectoryArg.extend_parser(self, parser)

        ig = parser.add_mutually_exclusive_group()
        ig.add_argument('-I',
                        '--id',
                        dest='actor_id',
                        type=str,
                        help='Actor identifier (overrides existing)')
        ig.add_argument('--force-create',
                        dest='force_create',
                        action='store_true',
                        help='Force creation of new Actor')

        parser.add_argument(
            '-E',
            '--env-file',
            default=ENVS_FILE,
            dest='envs_file',
            help='Environment variables JSON file (secrets.json)')

        parser.add_argument('-R',
                            '--dry-run',
                            dest='workflow_dry_run',
                            action='store_true',
                            help='Shortcut: Only build container')
        parser.add_argument('--ignore-errors',
                            dest='ignore_errors',
                            action='store_true',
                            help="Ignore deployment errors and warnings")
        parser.add_argument('--no-build',
                            dest='workflow_no_build',
                            action='store_false',
                            help="Do not build container image")
        parser.add_argument('--no-pull',
                            dest='workflow_no_pull',
                            action='store_false',
                            help="Do not pull source image when building")
        parser.add_argument('--no-push',
                            dest='workflow_no_push',
                            action='store_false',
                            help="Do not push built container image")
        parser.add_argument('--no-create',
                            dest='workflow_no_create',
                            action='store_false',
                            help="Do not create or update Tapis actor")
        parser.add_argument('--no-cache',
                            dest='workflow_no_cache',
                            action='store_false',
                            help="Do not cache the Tapis actor identifer")
        parser.add_argument('--no-grant',
                            dest='workflow_no_grant',
                            action='store_false',
                            help="Do not grant actor permissions")

        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.set_working_directory(parsed_args)
        self.docker_client_from_env()

        self.build = parsed_args.workflow_no_build
        self.pull = parsed_args.workflow_no_pull
        self.push = parsed_args.workflow_no_push
        self.create = parsed_args.workflow_no_create
        self.docache = parsed_args.workflow_no_cache
        self.grant = parsed_args.workflow_no_grant
        self.ignore_errors = parsed_args.ignore_errors

        # --dry-run is a shortcut for setting the following...
        if parsed_args.workflow_dry_run:
            self.build = True
            self.pull = True
            self.push = False
            self.create = False
            self.docache = False
            self.grant = False
            self.ignore_errors = False

        # if we don't build we should not push
        if self.build is False:
            self.push = False

        # Attempt to read from project.ini, then from reactor.rc
        # We do NOT merge them, and project.ini takes precedence
        config = self.get_ini_contents(parsed_args)
        if config == {}:
            config = rcfile.load_config(as_dict=True)
        if config == {}:
            raise WorkflowFailed('No project configuration found')

        # Validate minimim viable project configuration
        ACTOR_KEYS = ['name']
        DOCKER_KEYS = ['namespace', 'repo', 'tag']
        for k in ACTOR_KEYS:
            if config.get('actor', {}).get(k, None) is None:
                raise WorkflowFailed(
                    'actor#{0} missing from configuration'.format(k))
        for k in DOCKER_KEYS:
            if config.get('docker', {}).get(k, None) is None:
                raise WorkflowFailed(
                    'docker#{0} missing from configuration'.format(k))

        # Persist configuration for later
        self.config = config

        # Accept actorId from CLI first then from cache
        # Can still be None if no identifier can be resolved
        if parsed_args.actor_id is not None:
            self.actor_id = parsed_args.actor_id
        else:
            self.actor_id = actorid.read_id()

        # Read in environment vars from secrets.json
        self.envs = ActorsCreate.get_envs_from_file(parsed_args.envs_file,
                                                    decryption_key=None)

        # If Dockerfile is not present, turn off container workflow
        if not os.path.exists(self._dockerfile()):
            raise IOError('Dockerfile missing - project cannot be built')

        try:
            self._build(parsed_args)
            self._push(parsed_args)
            self._create(parsed_args)
            self._docache(parsed_args)
            self._grant(parsed_args)
        except Exception as exc:
            raise

        headers = ['stage', 'message']
        return (tuple(headers), tuple(self.messages))

    def _repo_tag(self):
        """Compute container repo:tag
        """
        # Look for registry, default to empty
        registry = self.config.get('docker', {}).get('registry', None)
        if registry == '':
            registry = None
        # Handle registry in URL or hostname form
        if registry is not None:
            parsed_url = urllib.parse.urlparse(registry)
            if parsed_url.netloc != '':
                registry = parsed_url.netloc
            elif parsed_url.path != '':
                registry = parsed_url.path

        docker_conf = self.config.get('docker', {})

        # Look for namespace, then default to empty
        namespace = docker_conf.get(
            'organization',
            docker_conf.get('namespace', docker_conf.get('username', None)))
        if namespace == '':
            namespace = None

        # Look for: docker.tag then default to empty
        tag = self.config.get('docker', {}).get('tag', None)
        if tag == '':
            tag = None

        # Look for docker.repo then default to empty
        repo = self.config.get('docker', {}).get('repo', None)
        if repo == '':
            repo = None
        if repo is None:
            raise WorkflowFailed('[docker]repo cannot be empty')

        if namespace is not None:
            # namespace/repo
            repo = namespace + '/' + repo
        if registry is not None:
            # registry/(namespace/?)repo
            repo = registry + '/' + repo
        if tag is not None:
            # (registry/?)(namespace/?)repo(:tag?)
            repo = repo + ':' + tag

        return repo

    def _dockerfile(self):
        """Compute path to application Dockerfile
        """
        # TODO - handle working directory
        return self.config.get('docker', {}).get('dockerfile', 'Dockerfile')

    def _build(self, parsed_args):
        """Build container
        """
        if self.build:
            try:
                tag = self._repo_tag()
                dockerfile = self._dockerfile()
                print_stderr('Building {}'.format(tag))
                start_time = milliseconds()
                # TODO - build_args, labels, nocache, quiet, forcerm
                result = self.dockerpy.images.build(path=self.working_dir,
                                                    tag=tag,
                                                    dockerfile=dockerfile,
                                                    pull=self.pull,
                                                    rm=True)
                print_stderr('Finished ({} msec)'.format(milliseconds() -
                                                         start_time))
                for log_line in result[1]:
                    txt = log_line.get('stream', '').strip()
                    if txt is not None and txt != '':
                        self.messages.append(
                            ('build', log_line.get('stream', None)))

                return True
            except Exception as err:
                if self.ignore_errors:
                    self.messages.append(('push', str(err)))
                    return False
                else:
                    raise

    def _push(self, parsed_args):
        """Push built container
        """
        if self.push:
            try:
                tag = self._repo_tag()
                print_stderr('Pushing {}'.format(tag))
                start_time = milliseconds()
                # TODO - auth_config
                for log_line in self.dockerpy.images.push(tag,
                                                          stream=True,
                                                          decode=True):
                    text_line = log_line.get('status', '').strip()
                    if text_line not in ('Preparing', 'Waiting',
                                         'Layer already exists', 'Pushing',
                                         'Pushed', ''):
                        self.messages.append(('push', text_line))
                print_stderr('Finished ({} msec)'.format(milliseconds() -
                                                         start_time))
                return True
            except Exception as err:
                if self.ignore_errors:
                    self.messages.append(('push', str(err)))
                    return False
                else:
                    raise

    def _create(self, parsed_args):
        """Create or update the actor
        """
        if self.create:
            try:

                # Here, document is the configuration JSON that will be
                # sent to the actors endpoint. In create/update, we build it
                # directly, but to accomodate the more declarative form of using
                # the .ini file, we have to do a few things differently.
                # Specifically, we read in a ConfigParser object then extend and/
                # or modify it until it the resulting dict is shaped correctly
                # to configure an Actor.
                document = self.config['actor']
                document['image'] = self._repo_tag()
                # Deploy ALWAYS forces an update to the actor
                document['force'] = True

                # Configure Actor's default environment as the right merge
                # of variables from project.ini[environment] and secrets.json
                # document['defaultEnvironment'] = self.envs
                union_envs = {**self.config['environment'], **self.envs}
                document['defaultEnvironment'] = union_envs

                # Configure Abaco cron from project.ini
                cron_schedule = document.pop('cron_schedule', None)
                cron_status = document.pop('cron_on', None)
                if cron_schedule is not None and cron_schedule != '':
                    document['cronSchedule'] = cron_schedule
                    # Override cron status via ini setting IF a schedule has been set
                    if cron_status is not None and cron_status != '':
                        document['cronOn'] = cron_status

                # Container UID
                cuid = document.pop('use_container_uid', None)
                if cuid is not None:
                    document['useContainerUid'] = parse_boolean(cuid)

                # Cast to booleans
                bool_keys = [
                    'privileged', 'stateless', 'token', 'useContainerUid',
                    'cronOn'
                ]
                for bk in bool_keys:
                    bkv = document.pop(bk, None)
                    if bkv is not None:
                        document[bk] = parse_boolean(bkv)

                if self.actor_id is None:
                    resp = self.tapis_client.actors.add(body=document)
                else:
                    resp = self.tapis_client.actors.update(
                        actorId=self.actor_id, body=document)

                actor_id = resp.get('id', None)
                setattr(self, 'actor_id', actor_id)

                self.messages.append(
                    ('create', 'Created Tapis actor {}'.format(actor_id)))
                return True

            except Exception as exc:
                if self.ignore_errors:
                    self.messages.append(('create', exc))
                    return False
                else:
                    raise

        return True

    def _docache(self, parsed_args):
        """Cache the actor identifier
        """
        if self.docache:
            actorid.write_id(self.actor_id)
            self.messages.append(('cache', 'Cached actor identifier to disk'))
        return True

    def _grant(self, parsed_args):
        """Grant access to designated users
        """
        if self.grant:
            granted = []
            for pem in [('update', 'UPDATE'), ('execute', 'EXECUTE'),
                        ('read', 'READ')]:
                users = self.config.get('grants', {}).get(pem[0],
                                                          '').split(',')
                users = [u.strip() for u in users]
                for u in users:
                    if u != '' and u not in granted:
                        body = {'username': u, 'permission': pem[1]}
                        resp = self.tapis_client.actors.updatePermissions(
                            actorId=self.actor_id, body=body)
                        self.messages.append(
                            ('grant-actor-pems', '{} {}'.format(u, pem[1])))
                        granted.append(u)
        return True
