from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatOne

__all__ = ['ProfilesShowSelf']


class ProfilesShowSelf(ProfilesFormatOne):

    HELP_STRING = 'Show Profile for the authenticated User'
    LEGACY_COMMMAND_STRING = 'profiles-list'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(Profile, parsed_args)
        rec = self.tapis_client.profiles.get()
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
