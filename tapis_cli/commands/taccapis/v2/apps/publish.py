from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsPublish']


class AppsPublish(AppsFormatOne, ServiceIdentifier):
    """Publish an app, making it generally usable across the platform
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsPublish, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser.add_argument(
            '-e',
            '--execution-system',
            type=str,
            dest='public_execution_system',
            help='Execution system where published app will run')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        headers = self.render_headers(App, parsed_args)

        mgt_body = {'action': 'publish'}
        if parsed_args.public_execution_system is not None:
            mgt_body['executionSystem'] = parsed_args.public_execution_system
        rec = self.tapis_client.apps.manage(appId=parsed_args.identifier,
                                            body=mgt_body)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
