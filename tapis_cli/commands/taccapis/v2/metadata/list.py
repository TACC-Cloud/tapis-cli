from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne, MetadataFormatMany

__all__ = ['MetadataList']


class MetadataList(MetadataFormatMany):
    """List the Metadata catalog
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(MetadataFormatMany, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        parsed_args = MetadataFormatMany.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, Metadata, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
