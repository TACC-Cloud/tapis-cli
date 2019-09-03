from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParamEqualsOnly as SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatOne, ProfilesFormatMany

__all__ = ['ProfilesList']


class ProfilesList(ProfilesFormatMany, SearchableCommand):
    """Search the Profiles catalog
    """
    VERBOSITY = Verbosity.LISTING

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        # raise SystemError(self.post_payload)

        results = self.requests_client.get_data(params=self.post_payload)
        headers = Profile().get_headers(self.VERBOSITY, parsed_args.formatter)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
