"""Metadata-specfic mixins
"""

from tapis_cli.clients.services.mixins import (ServiceIdentifier,
                                               InvalidIdentifier,
                                               UploadJsonFile,
                                               InvalidIdentifier)

__all__ = ['UploadMetadataFile']


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
