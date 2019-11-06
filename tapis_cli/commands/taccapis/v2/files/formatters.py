"""Formatters customized for system records and listings
"""
from tapis_cli.commands.taccapis.formatters import (TaccApisCommandBase,
                                                    TaccApisFormatOne,
                                                    TaccApisFormatMany)
from tapis_cli.clients.services.mixins import ParserExtender
from tapis_cli.utils import humanize_bytes
from .models import File

__all__ = [
    'FilesFormatOne', 'FilesFormatMany', 'FilesHistoryFormatMany',
    'FilesPemsFormatMany'
]


class FilesBase(TaccApisCommandBase):
    service_id_type = File.service_id_type

    def render_extended_parser_value(self,
                                     key,
                                     value,
                                     parsed_args,
                                     formatter=None):
        if formatter == 'table':
            if key in ('lastModified',
                       'lastUpdated') and parsed_args.ls_humanized:
                return key, value
            if key in ('length', 'size') and parsed_args.ls_humanized:
                return key, humanize_bytes(value)
        else:
            return key, value


class FilesFormatOne(FilesBase, TaccApisFormatOne):
    pass


class FilesFormatMany(FilesBase, TaccApisFormatMany):
    pass


class FilesHistoryFormatMany(FilesBase, TaccApisFormatMany):
    pass


class FilesPemsFormatMany(FilesBase, TaccApisFormatMany):
    pass
