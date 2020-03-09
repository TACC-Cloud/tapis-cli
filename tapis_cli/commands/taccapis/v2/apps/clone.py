from tapis_cli.display import Verbosity
from .mixins import AppIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsClone']


class AppsClone(AppsFormatOne, AppIdentifier):

    HELP_STRING = 'Clone an App'
    LEGACY_COMMMAND_STRING = 'apps-clone'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsClone, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        parser.add_argument(
            '-e',
            '--execution-system',
            type=str,
            dest='execution_system',
            help=
            "Execution system where the cloned app will run. Defaults to the current app's execution system."
        )
        parser.add_argument(
            '-s',
            '--deployment-system',
            type=str,
            dest='storage_system',
            help=
            "Storage system where the cloned app assets will be stored. Defaults to the current user's default storage system."
        )
        parser.add_argument(
            '-p',
            '--deployment-path',
            type=str,
            dest='storage_path',
            help=
            'Path on storage system where the cloned app assets will be stored. Only applies when cloning a public app.'
        )
        parser.add_argument(
            '-n',
            '--app-name',
            type=str,
            dest='app_name',
            help=
            "Optional new name of the cloned app. Defaults to the current App name and the authenticated user's username appended with a dash."
        )
        parser.add_argument(
            '-x',
            '--app-version',
            type=str,
            dest='app_version',
            help=
            "Optional new version of the cloned app. Defaults to the current app's version number."
        )
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        app_id = AppIdentifier.get_identifier(self, parsed_args)

        headers = self.render_headers(App, parsed_args)

        mgt_body = {'action': 'clone'}

        if parsed_args.app_name is not None:
            mgt_body['name'] = parsed_args.app_name
        if parsed_args.app_version is not None:
            mgt_body['version'] = parsed_args.app_version
        if parsed_args.execution_system is not None:
            mgt_body['executionSystem'] = parsed_args.execution_system
        if parsed_args.execution_system is not None:
            mgt_body['deploymentSystem'] = parsed_args.storage_system
        if parsed_args.execution_system is not None:
            mgt_body['deploymentPath'] = parsed_args.storage_path

        rec = self.tapis_client.apps.manage(appId=app_id, body=mgt_body)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
