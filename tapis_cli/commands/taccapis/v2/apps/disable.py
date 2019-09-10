from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsDisable']


class AppsDisable(AppsFormatOne, ServiceIdentifier):
    """Disable usage of an app
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = AppsFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = AppsFormatOne.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = SearchableCommand.headers(self, App, parsed_args)
        rec = self.tapis_client.apps.manage(appId=parsed_args.identifier,
                                            body={'action': 'disable'})
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
