"""Formatters customized for metadata records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from tapis_cli.clients.services.mixins import ServiceIdentifier
from .models import Metadata

__all__ = ['MetadataFormatOne', 'MetadataFormatMany']


class MetadataBase(TaccApisCommandBase):
    service_id_type = Metadata.service_id_type


class MetadataFormatOne(MetadataBase, TaccApisFormatOne):
    pass


class MetadataFormatMany(MetadataBase, TaccApisFormatMany):
    pass


