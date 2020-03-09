from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsEnable']


class SystemsEnable(SystemsFormatOne, ServiceIdentifier):

    HELP_STRING = 'Return a disabled System to active use'
    LEGACY_COMMMAND_STRING = 'systems-enable'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsEnable, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(System, parsed_args)
        rec = self.tapis_client.systems.manage(systemId=parsed_args.identifier,
                                               body={'action': 'enable'})

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
