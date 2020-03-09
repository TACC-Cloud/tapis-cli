from agavepy.agave import AgaveError
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier, Username

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne

__all__ = ['SystemsRolesShow']


class SystemsRolesShow(SystemsFormatOne, ServiceIdentifier, Username):

    HELP_STRING = 'Show roles on a System for the specified User'
    LEGACY_COMMMAND_STRING = 'systems-roles-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsRolesShow, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(SystemRole, parsed_args)
        try:
            rec = self.tapis_client.systems.getRoleForUser(
                systemId=parsed_args.identifier, username=parsed_args.username)
        except Exception:
            rec = {
                'username': parsed_args.username,
                'role': None,
                '_links': []
            }

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
