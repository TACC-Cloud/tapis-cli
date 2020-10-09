from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import MetadataFormatOne
from .mixins import MetadataUUID

__all__ = ['MetadataSchemaList']


class MetadataSchemaList(MetadataFormatOne, MetadataUUID):

    HELP_STRING = 'Retrieve Metadata Schemata'
    LEGACY_COMMMAND_STRING = 'metadata-schema-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        # uuid is metadata schema's uuid
        parser = super(MetadataSchemaList, self).get_parser(prog_name)
        parser = MetadataUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = MetadataUUID.get_identifier(self, parsed_args)
        self.update_payload(parsed_args)

        #headers = self.render_headers(Metadata, parsed_args)
        headers = ["uuid", "schema"]
        rec = self.tapis_client.meta.getSchema(
            uuid=identifier)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            key, val = self.render_extended_parser_value(key, val)
            data.append(val)
        return (tuple(headers), tuple(data))
