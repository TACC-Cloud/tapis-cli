"""Metadata-specfic mixins
"""

from tapis_cli.clients.services.mixins import (ServiceIdentifier,
                                               InvalidIdentifier,
                                               UploadJsonFile,
                                               InvalidIdentifier)

from tapis_cli.clients.services.mixins import InvalidValue, TapisEntityUUID

__all__ = ['UploadMetadataFile', 'MetadataUUID']


class MetadataExistsError(ValueError):
    pass


class UploadMetadataFile(UploadJsonFile):
    def extend_parser(self, parser):
        parser.add_argument('-F',
                            '--file',
                            dest='json_file_name',
                            metavar='<json_file>',
                            type=str,
                            help='JSON file containing document contents')
        return parser


class MetadataUUID(TapisEntityUUID):
    """Configures a command to require a mandatory Tapis metadata UUID
    """
    service_id_type = 'Metadata'
    dest = 'meta_uuid'
    suffix = '-012'
