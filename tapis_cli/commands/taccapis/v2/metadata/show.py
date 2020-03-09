from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import MetadataFormatOne
from .mixins import MetadataUUID
from .models import Metadata

__all__ = ['MetadataShow']


class MetadataShow(MetadataFormatOne, MetadataUUID):

    HELP_STRING = 'Show a Metadata document by UUID'
    LEGACY_COMMMAND_STRING = 'metadata-list'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(MetadataShow, self).get_parser(prog_name)
        parser = MetadataUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = MetadataUUID.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)

        headers = self.render_headers(Metadata, parsed_args)
        rec = self.tapis_client.meta.getMetadata(uuid=identifier)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            key, val = self.render_extended_parser_value(key, val)
            data.append(val)
        return (tuple(headers), tuple(data))
