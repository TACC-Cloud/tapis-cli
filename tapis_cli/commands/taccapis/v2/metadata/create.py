from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne
from .mixins import UploadMetadataFile
from .helpers import create_update, generate_name

__all__ = ['MetadataCreate']


class MetadataCreate(MetadataFormatOne, UploadMetadataFile):

    HELP_STRING = 'Store Metadata in a new document'
    LEGACY_COMMMAND_STRING = 'metadata-addupdate'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(MetadataCreate, self).get_parser(prog_name)
        name_group = parser.add_mutually_exclusive_group(required=False)
        parser.add_argument('-V',
                            '--value',
                            dest='meta_value',
                            metavar='Record value',
                            help='Value for the document')
        name_group.add_argument('-N',
                                '--name',
                                dest='meta_name',
                                metavar='Record name',
                                help='Optional name for the document')
        parser = UploadMetadataFile.extend_parser(self, parser)

        # name_group.add_argument('-A',
        #                         '--assign-name',
        #                         action='store_true',
        #                         help='Generate a name for the document')

        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)
        self.handle_file_upload(parsed_args)

        body = None
        if self.json_file_contents != {} and parsed_args.meta_value is not None:
            raise RuntimeError(
                'Specifing both --value and -F options is not supported.')

        # Blindly accept the JSON file if passed. Otherwise construct a
        # name/value record, generating the name if needed.
        if self.json_file_contents != {}:
            body = self.json_file_contents
        else:
            body = {'value': parsed_args.meta_value}
            if parsed_args.meta_name is not None:
                body['name'] = parsed_args.meta_name
            else:
                body['name'] = generate_name(
                    username=self.tapis_client.username,
                    data=parsed_args.meta_value)

        headers = self.render_headers(Metadata, parsed_args)
        rec = self.tapis_client.meta.addMetadata(body=body)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
