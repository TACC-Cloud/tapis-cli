"""Formatters customized for system records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany)
from tapis_cli.clients.services.mixins import ParserExtender
from tapis_cli.utils import humanize_bytes
from .models import File

__all__ = [
    'FilesFormatOne', 'FilesFormatMany', 'FilesHistoryFormatMany',
    'FileOptions', 'FilesOptions'
]


class FilesBase(TaccApisCommandBase):
    service_id_type = File.service_id_type


class FileOptions(ParserExtender):
    def extend_parser(self, parser):
        # parser.add_argument('--all',
        #                     dest='ls_all',
        #                     action='store_true',
        #                     help='Include directory entries whose names begin with a dot.')
        # parser.add_argument('--long',
        #                     dest='ls_long',
        #                     action='store_true',
        #                     help='List in long format.')
        # parser.add_argument('--humanize',
        #                     dest='ls_humanized',
        #                     action='store_true',
        #                     help='Display files sizes and time stamps in human terms')
        # parser.add_argument('--formatted',
        #                     dest='ls_formatted',
        #                     action='store_true',
        #                     help='Write a slash (/) after each filename if the file is a directory.')

        return parser

    def render_field(self, key, value, parsed_args, formatter=None):
        if formatter == 'table':
            if key in ('lastModified',
                       'lastUpdated') and parsed_args.ls_humanized:
                return key, value
            if key in ('length', 'size') and parsed_args.ls_humanized:
                return key, humanize_bytes(value)
        else:
            return key, value


class FilesOptions(FileOptions):
    def extend_parser(self, parser):
        parser = super().extend_parser(parser)
        parser.add_argument('--reverse',
                            dest='ls_sort_reverse',
                            action='store_true',
                            help='Reverse sort order.')
        parser.add_argument(
            '--sort-size',
            dest='ls_sort_size',
            action='store_true',
            help='Sort by size before sorting lexigraphically.')
        parser.add_argument(
            '--sort-time',
            dest='ls_sort_time',
            action='store_true',
            help='Sort by time modified before sorting lexigraphically.')
        return parser

    @classmethod
    def sort_table(cls, data, headers, header='name', reverse=False):
        user_idx = headers.index(header)
        path_idx = headers.index('name')
        # This will be the same position in the 'data' list
        sorted_data = sorted(data,
                             key=lambda x: (x[user_idx], x[path_idx]),
                             reverse=reverse)
        return sorted_data


class FilesFormatOne(FilesBase, TaccApisFormatOne):
    pass


class FilesFormatMany(FilesBase, TaccApisFormatMany):
    pass


class FilesHistoryFormatMany(FilesBase, TaccApisFormatMany):
    pass
