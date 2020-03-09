import docker as dockerpy
import os

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
        parser.add_argument('--dockerfile',
                            dest='docker_dockerfile',
                            metavar='DOCKERFILE',
                            type=str,
                            help='Dockerfile to build app repo')
        parser.add_argument('--docker-namespace',
                            dest='docker_namespace',
                            metavar='NAMESPACE',
                            type=str,
                            help='DockerHub namespace')
        parser.add_argument('--docker-repo',
                            dest='docker_repo',
                            metavar='REPO',
                            type=str,
                            help='Docker repo name')
        parser.add_argument('--docker-tag',
                            dest='docker_tag',
                            metavar='TAG',
                            type=str,
                            help='Docker repo tag')
        # Workflow control args
        parser.add_argument('-R',
                            '--dry-run',
                            dest='workflow_dry_run',
                            action='store_true',
                            help='Shortcut: Only build container')
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
        parser.add_argument('--no-grant',
                            dest='workflow_no_grant',
                            action='store_false',
                            help="Do not automatically do permission grant(s)")
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
        self.display = parsed_args.workflow_display

        # Shortcut
        if parsed_args.workflow_dry_run:
            self.build = True
            self.pull = True
            self.push = False
            self.backup = False
            self.upload = False
            self.create = False
            self.grant = False
            self.display = True

        # By passing a dict, we are able to override the contents of
        # the ini file
        self.passed_vals = {'docker': {}}
        if parsed_args.docker_namespace is not None:
            self.passed_vals['docker'][
                'namespace'] = parsed_args.docker_namespace
        if parsed_args.docker_repo is not None:
            self.passed_vals['docker']['repo'] = parsed_args.docker_repo
        if parsed_args.docker_tag is not None:
            self.passed_vals['docker']['tag'] = parsed_args.docker_tag
        self.config = self.all_key_values(parsed_args, self.passed_vals)

        # Override defaults
        # These allow options to be empty but receive default values from mandatory ones
        #
        # Force a container name to equal app.name if does not exist
        if self.config.get('docker', {}).get('repo', None) is None:
            self.config['docker']['repo'] = self.config['app']['name']
        # Force a tag to be app.version if does not exist
        if self.config.get('docker', {}).get('tag', None) is None:
            self.config['docker']['tag'] = self.config['app']['version']

        # If Dockerfile is not present, turn off container workflow
        if not os.path.exists(self._dockerfile()):
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

        # Look for namespace, then default to empty
        namespace = self.config.get('docker', {}).get('namespace', None)
        # Look for: docker.tag then default to empty
        tag = self.config.get('docker', {}).get('tag', None)
        # Look for docker.repo then default to empty
        repo = self.config.get('docker', {}).get('repo', None)

        if namespace is not None:
            repo = namespace + '/' + repo
        if tag is not None:
            repo = repo + ':' + tag
        return repo

    def _dockerfile(self):
        """Compute path to application Dockerfile
        """
        # TODO - handle working directory
        return self.config.get('docker', {}).get('dockerfile', 'Dockerfile')

    def _bundle(self):
        """Compute path to application asset bundle
        """
        # TODO - handle working directory
        # Default to DEFAULT_BUNDLE_NAME
        return self.config['app'].get('bundle', DEFAULT_BUNDLE_NAME)

    def _build(self, parsed_args):
        """Build container
        """
        if self.build:
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

    def _push(self, parsed_args):
        """Push built container
        """
        if self.push:
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
                manage.move(dep_path,
                            system_id=dep_sys,
                            destination=backup_dep_path,
                            agave=self.tapis_client)
                print_stderr('Finished ({} msec)'.format(milliseconds() -
                                                         start_time))
                return True
            except Exception as exc:
                self.messages.append(('backup', str(exc)))
                print_stderr('Failed ({} msec)'.format(milliseconds() -
                                                       start_time))
                return False

        return True

    def _upload(self, parsed_args):
        """Upload asset bundle
        """
        if self.upload:

            dep_sys = self.document['deploymentSystem']
            dep_path = self.document['deploymentPath']
            dep_path_parent = os.path.dirname(dep_path)
            dep_path_temp = os.path.join(dep_path_parent, self._bundle())

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
                # TODO - incorporate working directory
                manage.makedirs(dep_path_parent,
                                system_id=dep_sys,
                                permissive=True,
                                agave=self.tapis_client)
                manage.delete(dep_path,
                              system_id=dep_sys,
                              permissive=True,
                              agave=self.tapis_client)
                uploaded, skipped, errors, ul_bytes, ec_download = upload.upload(
                    self._bundle(),
                    system_id=dep_sys,
                    destination=dep_path_parent,
                    progress=True,
                    agave=self.tapis_client)
                manage.move(dep_path_temp,
                            system_id=dep_sys,
                            destination=dep_path,
                            agave=self.tapis_client)
                # Rename dep_path_parent/bundle to dep_path
                print_stderr('Finished ({} msec)'.format(milliseconds() -
                                                         start_time))
                for u in uploaded:
                    self.messages.append(('upload', u))
                for e in errors:
                    self.messages.append(('upload', e))
                return True

            except Exception as exc:
                self.messages.append(('upload', str(exc)))
                print_stderr('Failed ({} msec)'.format(milliseconds() -
                                                       start_time))
                return False

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
                self.messages.append(('create', exc))
                return False

        return True

    def _grant(self, parsed_args):
        """Grant access to designated users
        """
        if self.grant:
            granted = []
            for pem in [('update', 'ALL'), ('execute', 'READ_EXECUTE'),
                        ('read', 'READ')]:
                users = self.config['grants'].get(pem[0], '').split(',')
                users = [u.strip() for u in users]
                for u in users:
                    if u is not '' and u not in granted:
                        if pems.grant(self._app_id(),
                                      u,
                                      pem[1],
                                      permissive=False,
                                      agave=self.tapis_client) is not False:
                            self.messages.append(
                                ('grant', '{} {}'.format(u, pem[1])))
                            granted.append(u)
        return True
