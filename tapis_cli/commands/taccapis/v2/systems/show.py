from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.taccapis.v2.bearer import TapisServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsShow']


class SystemsShow(TapisServiceIdentifier, SystemsFormatOne):
    """Show a details about a system
    """
    VERBOSITY = Verbosity.RECORD

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = System().get_headers(self.VERBOSITY, parsed_args.formatter)

        rec = self.tapis_client.systems.get(systemId=parsed_args.identifier)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
