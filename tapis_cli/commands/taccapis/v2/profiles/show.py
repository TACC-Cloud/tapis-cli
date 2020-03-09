from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatOne

__all__ = ['ProfilesShow']


class ProfilesShow(ProfilesFormatOne, Username):

    HELP_STRING = 'Show details for a specific Profile'
    LEGACY_COMMMAND_STRING = 'profiles-list'

    VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ProfilesShow, self).get_parser(prog_name)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(Profile, parsed_args)
        rec = self.tapis_client.profiles.listByUsername(
            username=parsed_args.username)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
