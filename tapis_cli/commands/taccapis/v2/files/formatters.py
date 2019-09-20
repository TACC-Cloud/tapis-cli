"""Formatters customized for system records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany)
from .models import File

__all__ = ['FilesFormatOne', 'FilesFormatMany', 'FilesHistoryFormatMany']


class FilesBase(TaccApisCommandBase):
    service_id_type = File.service_id_type


class FilesFormatOne(FilesBase, TaccApisFormatOne):
    pass


class FilesFormatMany(FilesBase, TaccApisFormatMany):
    pass


class FilesHistoryFormatMany(FilesBase, TaccApisFormatMany):
    pass
