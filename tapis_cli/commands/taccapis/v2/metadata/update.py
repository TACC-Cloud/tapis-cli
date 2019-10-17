from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION

from .create import MetadataCreate
from .formatters import MetadataFormatOne
from .helpers import create_update, generate_name
from .models import Metadata
from .mixins import MetadataIdentifier, UploadMetadataFile


class MetadataUpdate(MetadataFormatOne, UploadMetadataFile,
                     MetadataIdentifier):
    """Update a metadata document by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = MetadataFormatOne.get_parser(self, prog_name)
        parser = UploadMetadataFile.extend_parser(self, parser)
        name_group = parser.add_mutually_exclusive_group(required=False)
        name_group.add_argument('-N',
                                '--rename',
                                dest='meta_name',
                                metavar='<record_name>',
                                help='Rename document')
        parser.add_argument('-V',
                            '--value',
                            dest='meta_value',
                            metavar='<record_value>',
                            help='Value for the document')
        parser = MetadataIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = super().preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)
        self.handle_file_upload(parsed_args)

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

        uuid_data = self.get_identifier(parsed_args, validate=True)

        headers = SearchableCommand.render_headers(self, Metadata, parsed_args)
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
