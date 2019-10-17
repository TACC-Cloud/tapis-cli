from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatOne

__all__ = ['ProfilesShow']


class ProfilesShow(ProfilesFormatOne, ServiceIdentifier):
    """Show a single user profile
    """
    VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = ProfilesFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = ProfilesFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = SearchableCommand.render_headers(self, Profile, parsed_args)
        rec = self.tapis_client.profiles.listByUsername(
            username=parsed_args.identifier)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
