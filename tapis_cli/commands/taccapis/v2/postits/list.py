from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import PostIt
from .formatters import PostItsFormatMany

__all__ = ['PostItsList']


class PostItsList(PostItsFormatMany):

    HELP_STRING = 'List active Post-Its'
    LEGACY_COMMMAND_STRING = 'postits-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(PostItsList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(PostIt, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
