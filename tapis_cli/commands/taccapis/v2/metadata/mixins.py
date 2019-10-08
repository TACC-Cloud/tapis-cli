"""Metadata-specfic mixins
"""

from tapis_cli.clients.services.mixins import (ServiceIdentifier,
                                               InvalidIdentifier)

__all__ = ['MetadataIdentifier']


class MetadataExistsError(ValueError):
    pass

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

    @classmethod
    def validate_identifier(cls, identifier):
        if True:
            return True
        else:
            raise InvalidIdentifier('{0} is not a valid identifier'.format(identifier))
