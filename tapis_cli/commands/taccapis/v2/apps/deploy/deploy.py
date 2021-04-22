import docker as dockerpy
import os
import urllib.parse
from datetime import datetime

from tapis_cli import settings
from tapis_cli.utils import (seconds, milliseconds, print_stderr)
from tapis_cli.project_ini.mixins import AppIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.commands.taccapis.v2.apps.create import AppsCreate
from tapis_cli.clients.services.mixins import (WorkingDirectoryArg,
                                               UploadJSONTemplate, DockerPy)
from tapis_cli.commands.taccapis.v2.files.helpers import manage, upload
from tapis_cli.commands.taccapis.v2.systems.helpers import default_execution_system, default_storage_system

from ..formatters import AppsFormatManyUnlimited
from .. import API_NAME, SERVICE_VERSION
from ..helpers import pems

__all__ = ['AppsDeploy']

DEFAULT_BUNDLE_NAME = 'assets'


class WorkflowFailed(Exception):
    pass


class UploadAppTemplate(UploadJSONTemplate):
    default = 'app.json'
    optional = True


# TODO - Identify and implement other run-time overrides as they make sense


class AppsDeploy(AppsFormatManyUnlimited, DockerPy, WorkingDirectoryArg,
                 UploadAppTemplate):

    HELP_STRING = 'Deploy an App from a project directory'
    LEGACY_COMMMAND_STRING = 'apps-deploy'

    config = {}
    document = None
    results = []
    messages = []
    passed_vals = {}

    # Workflow control flags
    build = True
    pull = True
    push = True
    backup = False
    upload = True
    create = True
    grant = True
    display = True

    def get_parser(self, prog_name):
        parser = super(AppsDeploy, self).get_parser(prog_name)
        # Mixins
        parser = WorkingDirectoryArg.extend_parser(self, parser)
        parser = UploadAppTemplate.extend_parser(self, parser)

        # Docker args
        # parser.add_argument('--dockerfile',
        #                     dest='docker_dockerfile',
        #                     metavar='DOCKERFILE',
        #                     type=str,
        #                     help='Dockerfile to build app repo')
        # parser.add_argument('--docker-namespace',
        #                     dest='docker_namespace',
        #                     metavar='NAMESPACE',
        #                     type=str,
        #                     help='DockerHub namespace')
        # parser.add_argument('--docker-repo',
        #                     dest='docker_repo',
        #                     metavar='REPO',
        #                     type=str,
        #                     help='Docker repo name')
        # parser.add_argument('--docker-tag',
        #                     dest='docker_tag',
        #                     metavar='TAG',
        #                     type=str,
        #                     help='Docker repo tag')
        # Workflow control args

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
        parser.add_argument('--backup',
                            dest='workflow_backup',
                            action='store_true',
                            help="Back up deployment path if present")
        parser.add_argument('--no-upload',
                            dest='workflow_no_upload',
                            action='store_false',
                            help="Do not upload app assets to Tapis storage")
        parser.add_argument('--no-create',
                            dest='workflow_no_create',
                            action='store_false',
                            help="Do not create a Tapis app record")
        parser.add_argument(
            '--no-grant',
            dest='workflow_no_grant',
            action='store_false',
            help="Do not automatically do application permission grant(s)")
        parser.add_argument(
            '--no-grant-roles',
            dest='workflow_no_grant_roles',
            action='store_false',
            help="Do not automatically do system role grant(s)")
        parser.add_argument('--display',
                            dest='workflow_display',
                            action='store_true',
                            help="Display rendered app in deployment log")

        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.set_working_directory(parsed_args)
        self.docker_client_from_env()

        self.build = parsed_args.workflow_no_build
        self.pull = parsed_args.workflow_no_pull
        self.push = parsed_args.workflow_no_push
        self.backup = parsed_args.workflow_backup
        self.upload = parsed_args.workflow_no_upload
        self.create = parsed_args.workflow_no_create
        self.grant = parsed_args.workflow_no_grant
        self.grant_roles = parsed_args.workflow_no_grant_roles
        self.display = parsed_args.workflow_display
        self.ignore_errors = parsed_args.ignore_errors

        # Do not grant system roles if permissions grant is disabled
        if self.grant is False:
            self.grant_roles = False

        # --dry-run is a shortcut for setting the following...
        if parsed_args.workflow_dry_run:
            self.build = True
            self.pull = True
            self.push = False
            self.backup = False
            self.upload = False
            self.create = False
            self.grant = False
            self.grant_roles = False
            self.display = True
            self.ignore_errors = False

        # By passing a dict, we are able to override the contents of
        # the ini file
        # self.passed_vals = {'docker': {}}
        # if parsed_args.docker_namespace is not None:
        #     self.passed_vals['docker'][
        #         'namespace'] = parsed_args.docker_namespace
        # if parsed_args.docker_repo is not None:
        #     self.passed_vals['docker']['repo'] = parsed_args.docker_repo
        # if parsed_args.docker_tag is not None:
        #     self.passed_vals['docker']['tag'] = parsed_args.docker_tag
        config = self.get_ini_contents(parsed_args)
        if config == {}:
            raise WorkflowFailed('No project configuration found')
        self.config = self.all_key_values(parsed_args, {})

        # Validate minimim viable project configuration
        APP_KEYS = ['name', 'version']
        for k in APP_KEYS:
            if config.get('app', {}).get(k, None) is None:
                raise WorkflowFailed(
                    'app#{0} missing from configuration'.format(k))

        # Construct a container repo name from app if not defined
        if self.config.get('docker', {}).get('repo', None) is None:
            self.config['docker']['repo'] = self.config['app']['name']
        # Force a tag to be app.version if does not exist
        if self.config.get('docker', {}).get('tag', None) is None:
            self.config['docker']['tag'] = self.config['app']['version']

        # Force population of docker config even if we don't build or
        # push the container in the current invocation of the deploy
        # command.
        self.docker_repo_string = self._repo_tag()

        # If Dockerfile is not present, turn off container workflow
        docker_path = os.path.join(self.working_dir, self._dockerfile())
        if not os.path.exists(docker_path):
            self.build = False
            self.pull = False
            self.push = False
            self.messages.append(
                ('build',
                 'Dockerfile not present. Skipped container actions.'))

        try:
            self._build(parsed_args)
            self._push(parsed_args)
            self._render(parsed_args)
            self._backup(parsed_args)
            self._upload(parsed_args)
            self._create(parsed_args)
            self._grant(parsed_args)
        except Exception as exc:
            raise

        headers = ['stage', 'message']
        return (tuple(headers), tuple(self.messages))

    def _app_id(self):
        """Compute the application ID
        """
        return '{}-{}'.format(self.config['app']['name'],
                              self.config['app']['version'])

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

        # Provide backwards compatibility for {{docker.organization}},
        # {{docker.namespace}} and {{docker.username}} when templating
        # out app.json on deployment
        #
        # I am not sure this is the right place to put this long-term since this
        # will not be availabel to other callers of JSON template rendering but
        # lets see if it fixes things for now...
        if registry is not None:
            template_namespace = registry + '/' + namespace
        else:
            template_namespace = namespace
        self.config['docker']['organization'] = template_namespace
        self.config['docker']['username'] = template_namespace
        self.config['docker']['namespace'] = template_namespace

        return repo

    def _dockerfile(self):
        """Compute path to application Dockerfile
        """
        return self.config.get('docker', {}).get('dockerfile', 'Dockerfile')

    def _bundle(self):
        """Compute path to application asset bundle
        """
        # Default to DEFAULT_BUNDLE_NAME
        bundle_path = os.path.join(self.working_dir, DEFAULT_BUNDLE_NAME)
        return self.config['app'].get('bundle', bundle_path)

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

    def _render(self, parsed_args):
        """Load and render app.json
        """
        self.handle_file_upload(parsed_args, passed_vals=self.config)
        setattr(self, 'document', self.json_file_contents)
        if self.display:
            self.messages.append(('render', self.document))
        return True

    def _backup(self, parsed_args):
        """Backup existing deployed assets
        """
        if self.backup:
            dep_sys = self.document['deploymentSystem']
            dep_path = self.document['deploymentPath']
            backup_dep_path = dep_path + '.' + str(seconds())

            print_stderr('Backing up agave://{}/{}'.format(dep_sys, dep_path))
            start_time = milliseconds()
            self.messages.append(
                ('backup', 'src: agave://{}/{}'.format(dep_sys, dep_path)))
            self.messages.append(
                ('backup', 'dst: agave://{}/{}'.format(dep_sys,
                                                       backup_dep_path)))

            try:
                # TODO - only do this if dep_path exists, otherwise an Exception will be raised
                manage.move(dep_path,
                            system_id=dep_sys,
                            destination=backup_dep_path,
                            agave=self.tapis_client)
                print_stderr('Finished ({} msec)'.format(milliseconds() -
                                                         start_time))
                return True
            except Exception as exc:
                if self.ignore_errors:
                    self.messages.append(('backup', str(exc)))
                    print_stderr('Failed ({} msec)'.format(milliseconds() -
                                                           start_time))
                    return False
                else:
                    raise

        return True

    def _upload(self, parsed_args):
        """Upload asset bundle
        """
        if self.upload:

            dep_sys = self.document['deploymentSystem']
            dep_path = self.document['deploymentPath']
            dep_path_parent = os.path.dirname(dep_path)
            # need the bundle basename for the upload/move workflow to work
            bundle_basename = os.path.basename(os.path.normpath(
                self._bundle()))
            # add date to make tmpdir unique from bundle and deploymentPath
            dep_path_temp = os.path.join(dep_path_parent, bundle_basename) \
                + datetime.now().strftime("-%Y-%m-%d")
            print_stderr(
                'Uploading app asset directory "{0}" to agave://{1}/{2}'.
                format(self._bundle(), dep_sys, dep_path))

            start_time = milliseconds()
            try:
                # First, check existence of bundle. No point in taking other action
                # if it does not exist
                if not os.path.exists(self._bundle()):
                    raise FileNotFoundError(
                        'Unable to locate asset directory "{}"'.format(
                            self._bundle()))
                try:
                    # need relative destination here because
                    # agavepy permissions check will fail on '/'
                    # for public systems
                    manage.makedirs(os.path.basename(dep_path_temp),
                                    system_id=dep_sys,
                                    permissive=True,
                                    destination=dep_path_parent,
                                    agave=self.tapis_client)
                    # clear out destination directory
                    manage.delete(dep_path,
                                  system_id=dep_sys,
                                  permissive=True,
                                  agave=self.tapis_client)
                except Exception as err:
                    self.messages.append(('upload', str(err)))
                # upload bundle to tmp dir
                uploaded, skipped, errors, ul_bytes, ec_download = upload.upload(
                    self._bundle(),
                    system_id=dep_sys,
                    destination=dep_path_temp,
                    progress=True,
                    agave=self.tapis_client)
                # move tmp dir bundle to the destination dir
                manage.move(os.path.join(dep_path_temp, bundle_basename),
                            system_id=dep_sys,
                            destination=dep_path,
                            agave=self.tapis_client)
                # delete tmp dir
                manage.delete(dep_path_temp,
                              system_id=dep_sys,
                              permissive=True,
                              agave=self.tapis_client)
                print_stderr('Finished ({} msec)'.format(milliseconds() -
                                                         start_time))
                for u in uploaded:
                    self.messages.append(('upload', u))
                for e in errors:
                    self.messages.append(('upload', e))
                if len(errors) > 0:
                    if self.ignore_errors is False:
                        raise Exception('Upload failures: {}'.format(
                            errors.join(';')))
                return True

            except Exception as exc:
                if self.ignore_errors:
                    self.messages.append(('upload', str(exc)))
                    print_stderr('Failed ({} msec)'.format(milliseconds() -
                                                           start_time))
                    return False
                else:
                    raise

        return True

    def _create(self, parsed_args):
        """Create or update the app representation
        """
        if self.create:
            try:
                resp = self.tapis_client.apps.add(body=self.document)
                self.messages.append(
                    ('create', 'Created Tapis app {} revision {}'.format(
                        resp.get('id'), resp.get('revision'))))
                return True
            except Exception as exc:
                if self.ignore_errors:
                    self.messages.append(('create', exc))
                    return False
                else:
                    raise

        return True

    def _grant(self, parsed_args):
        """Grant app access to designated users
        """
        if self.grant:
            granted = []
            for pem in [('update', 'ALL'), ('execute', 'READ_EXECUTE'),
                        ('read', 'READ')]:
                users = self.config['grants'].get(pem[0], '').split(',')
                users = [u.strip() for u in users]
                for u in users:
                    if u != '' and u not in granted:
                        if pems.grant(self._app_id(),
                                      u,
                                      pem[1],
                                      grant_system_roles=self.grant_roles,
                                      permissive=False,
                                      agave=self.tapis_client) is not False:
                            self.messages.append(
                                ('grant-app-pems', '{} {}'.format(u, pem[1])))
                            # Technically this message indicates the attempt not the successful role grant
                            if self.grant_roles:
                                self.messages.append(('grant-system-roles',
                                                      '{} USER'.format(u)))
                            granted.append(u)
        return True
