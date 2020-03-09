from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import AppsFormatOne
from .mixins import AppIdentifier
from .models import App

__all__ = ['AppsShow']


class AppsShow(AppsFormatOne, AppIdentifier):

    HELP_STRING = 'Show details for an App'
    LEGACY_COMMMAND_STRING = 'apps-list'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(AppsShow, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(App, parsed_args)
        rec = self.tapis_client.apps.get(appId=app_id)

        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
