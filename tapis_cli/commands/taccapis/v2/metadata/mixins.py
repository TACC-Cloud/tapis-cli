"""Metadata-specfic mixins
"""

from tapis_cli.clients.services.mixins import (ServiceIdentifier,
                                               InvalidIdentifier,
                                               UploadJSONTemplate,
                                               InvalidIdentifier)

from tapis_cli.clients.services.mixins import InvalidValue, TapisEntityUUID

__all__ = ['UploadMetadataFile', 'MetadataUUID']


class MetadataExistsError(ValueError):
    pass


class UploadMetadataFile(UploadJSONTemplate):
    optional = True


class MetadataUUID(TapisEntityUUID):
    """Configures a command to require a mandatory Tapis metadata UUID
    """
    optional = False
    service_id_type = 'Metadata'
    dest = 'meta_uuid'
    suffix = '-012'
