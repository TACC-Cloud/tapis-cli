from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsShow']


class AppsShow(AppsFormatOne):
    """Show a single app record
    """
    VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsFormatOne, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = App().get_headers(self.VERBOSITY, parsed_args.formatter)
        rec = self.tapis_client.apps.get(appId=parsed_args.identifier)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
