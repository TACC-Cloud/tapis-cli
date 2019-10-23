"""Metadata-specfic mixins
"""

from tapis_cli.clients.services.mixins import (ServiceIdentifier,
                                               InvalidIdentifier,
                                               UploadJsonFile,
                                               InvalidIdentifier)

__all__ = ['MetadataIdentifier', 'UploadMetadataFile']


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


class MetadataIdentifier(ServiceIdentifier):
    @classmethod
    def arg_display(cls, id_value):
        return '<uuid>'.format(id_value).lower()

    @classmethod
    def arg_metavar(cls, id_value):
        return cls.arg_display(id_value)

    @classmethod
    def arg_help(cls, id_value):
        return 'Metadata UUID'.format(id_value)

    def validate_identifier(self, identifier, permissive=False):
        if len(identifier) >= 36 and len(
                identifier) <= 40 and identifier.endswith('-012'):
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidIdentifier(
                    '{0} not a valid metadata UUID'.format(identifier))
