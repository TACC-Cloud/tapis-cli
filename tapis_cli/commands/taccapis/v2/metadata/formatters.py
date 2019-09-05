"""Formatters customized for metadata records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from .models import Metadata

__all__ = ['MetadataFormatOne', 'MetadataFormatMany']


class MetadataBase(TaccApisBase):
    id_display_name = Metadata.id_display_name


class MetadataFormatOne(TaccApisFormatOne, MetadataBase):
    pass


class MetadataFormatMany(TaccApisFormatMany, MetadataBase):
    pass
