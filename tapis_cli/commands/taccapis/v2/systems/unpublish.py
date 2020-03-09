from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsUnpublish']


class SystemsUnpublish(SystemsFormatOne, ServiceIdentifier):

    HELP_STRING = 'Unpublish a public System'
    LEGACY_COMMMAND_STRING = 'systems-unpublish'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsFormatOne, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = SearchableCommand.render_headers(self, System, parsed_args)
        rec = self.tapis_client.systems.manage(systemId=parsed_args.identifier,
                                               body={'action': 'unpublish'})

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
