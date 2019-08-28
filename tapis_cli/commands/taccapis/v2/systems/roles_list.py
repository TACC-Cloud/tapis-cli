from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne, SystemsFormatMany

__all__ = ['SystemsRolesList']


class SystemsRolesList(SystemsFormatMany):
    """List roles on a specific system
    """
    VERBOSITY = Verbosity.BRIEF
    id_display_name = 'SYSTEM_ID'

    def get_parser(self, prog_name):
        parser = super(SystemsRolesList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        results = self.tapis_client.systems.listRoles(
            systemId=parsed_args.identifier)
        headers = SystemRole().get_headers(self.VERBOSITY)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
