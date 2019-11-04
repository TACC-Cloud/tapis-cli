"""Formatters customized for metadata records and listings
"""
from tapis_cli.commands.taccapis.formatters import (TaccApisCommandBase,
                                                    TaccApisFormatOne,
                                                    TaccApisFormatMany)
from .models import Metadata

__all__ = ['MetadataFormatOne', 'MetadataFormatMany']


class MetadataBase(TaccApisCommandBase):
    pass


class MetadataFormatOne(MetadataBase, TaccApisFormatOne):
    pass


class MetadataFormatMany(MetadataBase, TaccApisFormatMany):
    pass
