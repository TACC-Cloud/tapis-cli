from agavepy.agave import AgaveError
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne

__all__ = ['SystemsRolesRevoke']


class SystemsRolesRevoke(SystemsFormatOne, ServiceIdentifier):
    """Revoke the current role for a User on a System
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = SystemsFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser.add_argument('username',
                            metavar='<username>',
                            type=str,
                            help='Revokee username')
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        # List roles on the System to show the new role
        headers = SearchableCommand.headers(self, SystemRole, parsed_args)
        rec = self.tapis_client.systems.deleteRoleForUser(
            systemId=parsed_args.identifier, username=parsed_args.username)

        if rec is None:
            data = [parsed_args.username, None]
        else:
            raise AgaveError('Failed to revoke role from {0}'.format(
                parsed_args.identifier))

        return (tuple(headers), tuple(data))
