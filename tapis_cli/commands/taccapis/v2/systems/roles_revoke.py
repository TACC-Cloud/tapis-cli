from agavepy.agave import AgaveError
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier, Username

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne

__all__ = ['SystemsRolesRevoke']


class SystemsRolesRevoke(SystemsFormatOne, ServiceIdentifier, Username):

    HELP_STRING = 'Revoke a user role from a System'
    LEGACY_COMMMAND_STRING = 'systems-roles-addupdate'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsRolesRevoke, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        # List roles on the System to show the new role
        headers = self.render_headers(SystemRole, parsed_args)
        rec = self.tapis_client.systems.deleteRoleForUser(
            systemId=parsed_args.identifier, username=parsed_args.username)

        if rec is None:
            data = [parsed_args.username, None]
        else:
            raise AgaveError('Failed to revoke role from {0}'.format(
                parsed_args.identifier))

        return (tuple(headers), tuple(data))
