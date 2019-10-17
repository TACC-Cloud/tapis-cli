from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatMany

__all__ = ['ProfilesList']


class ProfilesList(ProfilesFormatMany):
    """Search the Profiles catalog
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.LISTING

    def take_action(self, parsed_args):
        parsed_args = ProfilesFormatMany.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, Profile, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
