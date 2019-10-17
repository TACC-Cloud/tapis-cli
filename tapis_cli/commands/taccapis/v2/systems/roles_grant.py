from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne

__all__ = ['SystemsRolesGrant']


class SystemsRolesGrant(SystemsFormatOne, ServiceIdentifier):
    """Grant a role on an System to a User
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = SystemsFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser.add_argument('username',
                            metavar='<username>',
                            type=str,
                            help='Grantee username')
        parser.add_argument('role',
                            type=str,
                            metavar='<permission>',
                            choices=SystemRole.NAMES,
                            help='Role ({0})'.format('| '.join(
                                SystemRole.NAMES)))
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        role = parsed_args.role
        body = {'username': parsed_args.username, 'role': role.upper()}

        # List roles on the System to show the new role
        headers = SearchableCommand.render_headers(self, SystemRole,
                                                   parsed_args)
        rec = self.tapis_client.systems.updateRole(
            systemId=parsed_args.identifier, body=body)[0]

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
