from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne
from .mixins import UploadMetadataFile
from .helpers import create_update, generate_name

__all__ = ['MetadataCreate']


class MetadataCreate(MetadataFormatOne, UploadMetadataFile):
    """Create a Metadata document
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(MetadataCreate, self).get_parser(prog_name)
        parser = UploadMetadataFile.extend_parser(self, parser)
        name_group = parser.add_mutually_exclusive_group(required=False)
        name_group.add_argument('-N',
                                '--name',
                                dest='meta_name',
                                metavar='Record name',
                                help='Name of the document')
        name_group.add_argument('-A',
                                '--assign-name',
                                action='store_true',
                                help='Generate a name for the document')
        parser.add_argument('-V',
                            '--value',
                            dest='meta_value',
                            metavar='Record value',
                            help='Value for the document')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
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

        if parsed_args.meta_name is not None:
            name_data = parsed_args.meta_name
        else:
            name_data = generate_name(username=self.tapis_client.username,
                                      data=value_data)

        headers = self.render_headers(Metadata, parsed_args)
        rec = create_update(name=name_data,
                            value=value_data,
                            uuid=None,
                            permissive=False,
                            agave=self.tapis_client)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
