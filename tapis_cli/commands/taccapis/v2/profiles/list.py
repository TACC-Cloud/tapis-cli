from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatMany

__all__ = ['ProfilesList']


class ProfilesList(ProfilesFormatMany):
    """List all Profiles (requires administrative privileges)
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.LISTING

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(Profile, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
