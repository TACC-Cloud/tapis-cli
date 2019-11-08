from tapis_cli.display import Verbosity

from .create import MetadataCreate
from .formatters import MetadataFormatOne
from .helpers import create_update, generate_name
from .models import Metadata
from .mixins import MetadataUUID
from .mixins import UploadMetadataFile
from . import API_NAME, SERVICE_VERSION


class MetadataUpdate(MetadataFormatOne, UploadMetadataFile, MetadataUUID):
    """Update an existing Metadata document by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(MetadataUpdate, self).get_parser(prog_name)
        name_group = parser.add_mutually_exclusive_group(required=False)
        parser.add_argument('-V',
                            '--value',
                            dest='meta_value',
                            metavar='<record_value>',
                            help='Value for the document')
        name_group.add_argument('-N',
                                '--rename',
                                dest='meta_name',
                                metavar='<record_name>',
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

        self.value_data = None
        if parsed_args.json_file_name is not None and parsed_args.meta_value is not None:
            raise RuntimeError(
                'Specifing both --value and -F options is not supported.')
        else:
            if parsed_args.meta_value is not None:
                value_data = parsed_args.meta_value
            else:
                value_data = self.json_file_contents

        persist_name = True
        if parsed_args.meta_name is not None:
            name_data = parsed_args.meta_name
            persist_name = False
        else:
            name_data = None

        uuid_data = identifier

        headers = self.render_headers(Metadata, parsed_args)
        rec = create_update(name=name_data,
                            value=value_data,
                            uuid=uuid_data,
                            peristent_name=persist_name,
                            permissive=False,
                            agave=self.tapis_client)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
