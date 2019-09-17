"""Formatters customized for metadata records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from tapis_cli.clients.services.mixins import ServiceIdentifier
from .models import Metadata

__all__ = ['MetadataFormatOne', 'MetadataFormatMany', 'MetadataIdentifier']


class MetadataBase(TaccApisCommandBase):
    service_id_type = Metadata.service_id_type


class MetadataFormatOne(MetadataBase, TaccApisFormatOne):
    pass


class MetadataFormatMany(MetadataBase, TaccApisFormatMany):
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
