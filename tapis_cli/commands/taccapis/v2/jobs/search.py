from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatMany

__all__ = ['JobsSearch']


class JobsSearch(JobsFormatMany):

    HELP_STRING = 'Search Job records'
    LEGACY_COMMMAND_STRING = 'jobs-search'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING

    def get_parser(self, prog_name):
        parser = super(JobsSearch, self).get_parser(prog_name)
        parser = SearchableCommand.extend_parser(self, parser, Job)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        # Map properties set in parsed_args to a query payload for search
        filters = []
        for sarg_name, sarg in self.search_args.items():
            parsed_args_val = getattr(parsed_args, sarg.destination, None)
            if parsed_args_val:
                filt = sarg.get_param(parsed_args_val)
                filters.append(filt)

        for f in filters:
            k = list(f.keys())[0]
            v = f[k]
            self.post_payload[k] = v

        headers = self.render_headers(Job, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
