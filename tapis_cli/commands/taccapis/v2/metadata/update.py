from tapis_cli.display import Verbosity

from .create import MetadataCreate
from .formatters import MetadataFormatOne
from .helpers import create_update, generate_name
from .models import Metadata
from .mixins import MetadataUUID
from .mixins import UploadMetadataFile
from . import API_NAME, SERVICE_VERSION


class MetadataUpdate(MetadataFormatOne, UploadMetadataFile, MetadataUUID):

    HELP_STRING = 'Update an existing Metadata document by UUID'
    LEGACY_COMMMAND_STRING = 'metadata-addupdate'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(MetadataUpdate, self).get_parser(prog_name)
        name_group = parser.add_mutually_exclusive_group(required=False)
        parser.add_argument('-V',
                            '--value',
                            dest='meta_value',
                            metavar='VALUE',
                            help='Value for the document')
        name_group.add_argument('-N',
                                '--rename',
                                dest='meta_name',
                                metavar='NEW_NAME',
                                help='Rename document')
        parser = UploadMetadataFile.extend_parser(self, parser)
        parser = MetadataUUID.extend_parser(self, parser)

        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)
        self.handle_file_upload(parsed_args)
        identifier = MetadataUUID.get_identifier(self, parsed_args)

        body = None
        if self.json_file_contents != {} and parsed_args.meta_value is not None:
            raise RuntimeError(
                'Specifing both --value and -F options is not supported.')

        # Blindly accept the JSON file if passed. Otherwise construct a
        # name/value record, generating the name if needed.
        if self.json_file_contents != {}:
            body = self.json_file_contents
        else:
            # Fetch
            doc = self.tapis_client.meta.getMetadata(uuid=identifier)
            body = {
                'name': doc.get('name'),
                'value': doc.get('value'),
                'associationIds': doc.get('associationIds', [])
            }
            if parsed_args.meta_name is not None:
                body['name'] = parsed_args.meta_name
            if parsed_args.meta_value is not None:
                body['value'] = parsed_args.meta_value

        headers = self.render_headers(Metadata, parsed_args)
        rec = self.tapis_client.meta.updateMetadata(body=body, uuid=identifier)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
