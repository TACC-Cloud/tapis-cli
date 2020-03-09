from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatMany

__all__ = ['SystemsRolesList']


class SystemsRolesList(SystemsFormatMany, ServiceIdentifier):

    HELP_STRING = 'List user roles on a System'
    LEGACY_COMMMAND_STRING = 'systems-roles-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsRolesList, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(SystemRole, parsed_args)
        results = self.tapis_client.systems.listRoles(
            systemId=parsed_args.identifier)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
