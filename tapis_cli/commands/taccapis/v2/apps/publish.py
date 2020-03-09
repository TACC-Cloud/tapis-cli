from tapis_cli.display import Verbosity
from .mixins import AppIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsPublish']


class AppsPublish(AppsFormatOne, AppIdentifier):

    HELP_STRING = 'Publish an App for use by others'
    LEGACY_COMMMAND_STRING = 'apps-publish'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsPublish, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        parser.add_argument(
            '-e',
            '--execution-system',
            type=str,
            dest='public_execution_system',
            help='Optional execution system where the public app will run')
        parser.add_argument('-n',
                            '--app-name',
                            type=str,
                            dest='app_name',
                            help='Optional new name of the public app')
        parser.add_argument('-x',
                            '--app-version',
                            type=str,
                            dest='app_version',
                            help='Optional new version of the public app')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        mgt_body = {'action': 'publish'}

        if parsed_args.app_name is not None:
            mgt_body['name'] = parsed_args.app_name
        if parsed_args.app_version is not None:
            mgt_body['version'] = parsed_args.app_version
        if parsed_args.public_execution_system is not None:
            mgt_body['executionSystem'] = parsed_args.public_execution_system

        headers = self.render_headers(App, parsed_args)
        rec = self.tapis_client.apps.manage(appId=app_id, body=mgt_body)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
