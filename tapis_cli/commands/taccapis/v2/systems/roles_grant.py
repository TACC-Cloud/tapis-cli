from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier, Username

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne

__all__ = ['SystemsRolesGrant']


class SystemsRolesGrant(SystemsFormatOne, ServiceIdentifier, Username):

    HELP_STRING = 'Grant a user role on a System'
    LEGACY_COMMMAND_STRING = 'systems-roles-addupdate'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsRolesGrant, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)

        parser.add_argument('role',
                            type=str,
                            metavar='ROLE',
                            choices=SystemRole.NAMES,
                            help='Role ({0})'.format('| '.join(
                                SystemRole.NAMES)))
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        role = parsed_args.role
        body = {'username': parsed_args.username, 'role': role.upper()}

        # List roles on the System to show the new role
        headers = self.render_headers(SystemRole, parsed_args)
        rec = self.tapis_client.systems.updateRole(
            systemId=parsed_args.identifier, body=body)[0]

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
