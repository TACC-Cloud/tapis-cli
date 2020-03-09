from tapis_cli.display import Verbosity
from .mixins import AppIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsDisable']


class AppsDisable(AppsFormatOne, AppIdentifier):

    HELP_STRING = 'Disable usage of an App'
    LEGACY_COMMMAND_STRING = 'apps-disable'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsDisable, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(App, parsed_args)
        rec = self.tapis_client.apps.manage(appId=app_id,
                                            body={'action': 'disable'})
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
