from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne, AppsFormatMany

__all__ = ['AppsSearch']


class AppsSearch(AppsFormatMany):

    HELP_STRING = 'Search the Apps catalog'
    LEGACY_COMMMAND_STRING = 'apps-list'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.LISTING

    def get_parser(self, prog_name):
        parser = super(AppsSearch, self).get_parser(prog_name)
        parser = SearchableCommand.extend_parser(self, parser, App)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        # Map properties set in parsed_args to a query payload for search
        filters = list()
        for sarg_name, sarg in self.search_args.items():
            # raise SystemError(sarg.destination)
            parsed_args_val = getattr(parsed_args, sarg.destination, None)
            if parsed_args_val:
                filt = sarg.get_param(parsed_args_val)
                filters.append(filt)

        for f in filters:
            k = list(f.keys())[0]
            v = f[k]
            self.post_payload[k] = v

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
