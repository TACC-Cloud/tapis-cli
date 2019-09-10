from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatMany

__all__ = ['AppsList']


class AppsList(AppsFormatMany):
    """List the Apps catalog
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING

    def take_action(self, parsed_args):
        parsed_args = AppsFormatMany.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = SearchableCommand.headers(self, App, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
