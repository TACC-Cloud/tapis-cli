from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne, MetadataFormatMany

__all__ = ['MetadataList']


class MetadataList(MetadataFormatMany):

    HELP_STRING = 'List Metadata documents'
    LEGACY_COMMMAND_STRING = 'metadata-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(MetadataList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)

        headers = self.render_headers(Metadata, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
