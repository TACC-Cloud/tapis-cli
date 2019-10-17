from agavepy.agave import AgaveError
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatOne

__all__ = ['SystemsRolesShow']


class SystemsRolesShow(SystemsFormatOne, ServiceIdentifier):
    """Show role on a System for a User
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = SystemsFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser.add_argument('username',
                            metavar='<username>',
                            type=str,
                            help='Username to show role for')
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, SystemRole, parsed_args)
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
