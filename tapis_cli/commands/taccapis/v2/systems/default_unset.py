from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsDefaultUnset']


class SystemsDefaultUnset(SystemsFormatOne, ServiceIdentifier):

    HELP_STRING = "Unset a Tapis System as the user's (or global) default"
    LEGACY_COMMMAND_STRING = 'systems-unsetdefault'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsDefaultUnset, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser.add_argument(
            '-G',
            dest='global_default',
            action='store_true',
            help='Unset tenant-wide default (requires admin rights)')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        if parsed_args.global_default:
            action = 'unsetGlobalDefault'
        else:
            action = 'unsetDefault'
        headers = self.render_headers(System, parsed_args)
        rec = self.tapis_client.systems.manage(systemId=parsed_args.identifier,
                                               body={'action': action})

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
