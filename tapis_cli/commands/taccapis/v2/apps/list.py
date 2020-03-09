from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatMany

__all__ = ['AppsList']


class AppsList(AppsFormatMany):

    HELP_STRING = 'List the Apps catalog'
    LEGACY_COMMMAND_STRING = 'apps-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(App, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
