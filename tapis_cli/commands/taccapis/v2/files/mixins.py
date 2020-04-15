"""Files-specfic mixins
"""

from tapis_cli.clients.services.mixins import ParserExtender

__all__ = [
    'ExcludeFiles', 'FileOptions', 'FilesOptions', 'FilesCallbackURI',
    'IncludeFiles', 'OverwritePolicy', 'ReportProgress'
]


class ExcludeFiles(ParserExtender):
    """Configures a Command to accept a list of files to exclude

    Sets 'parsed_args.exclude_files'
    """
    def extend_parser(self, parser):
        parser.add_argument(
            '--exclude',
            dest='exclude_files',
            action='append',
            metavar='GLOB',
            help='Unix-style fileglob (specify multiple times)')
        return parser


class IncludeFiles(ParserExtender):
    """Configures a Command to accept a list of files to include

    Sets 'parsed_args.include_files'
    """
    def extend_parser(self, parser):
        parser.add_argument(
            '--include',
            dest='include_files',
            action='append',
            metavar='GLOB',
            help='Unix-style fileglob (specify multiple times)')
        return parser


class FilesCallbackURI(ParserExtender):
    """Configures a Command to accept a URI to call when a files action is complete

    Sets 'parsed_args.files_callback_uri'
    """
    def extend_parser(self, parser):
        parser.add_argument(
            '--callback',
            dest='files_callback_uri',
            metavar='URI',
            help=
            "A URI to notify when each upload import is complete. Can be an email address or http/s URL. If a URL is given, a GET will be made."
        )
        return parser


class FileOptions(ParserExtender):
    """Configures a Command to accept rendering options for a single file
    """
    def extend_parser(self, parser):
        parser.add_argument('--all',
                            dest='dotfiles',
                            action='store_true',
                            help='Include hidden files')
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


class FilesOptions(FileOptions):
    """Configures a Command to accept rendering options for a list of files

    Extends parser to set 'parsed_args.ls_sort_reverse',
    'parsed_args.ls_sort_size', and 'parsed_args.ls_sort_time'. Also provides
    a 'sort_table' function to sort a table by designated header.
    """
    def extend_parser(self, parser):
        parser = super(FilesOptions, self).extend_parser(parser)
        parser.add_argument('--reverse',
                            dest='ls_sort_reverse',
                            action='store_true',
                            help='Reverse sort order.')
        sort_field = parser.add_mutually_exclusive_group(required=False)
        sort_field.add_argument(
            '--sort-size',
            dest='ls_sort_size',
            action='store_true',
            help='Sort by size before sorting lexicographically.')
        sort_field.add_argument(
            '--sort-time',
            dest='ls_sort_time',
            action='store_true',
            help='Sort by time modified before sorting lexicographically.')
        return parser

    @classmethod
    def sort_table(cls, rows, headers, header='name', reverse=False):
        user_idx = headers.index(header)
        path_idx = headers.index('name')
        # This will be the same position in the 'data' list
        sorted_data = sorted(rows,
                             key=lambda x: (x[user_idx], x[path_idx]),
                             reverse=reverse)
        return sorted_data


class OverwritePolicy(ParserExtender):
    """Configures a Command to allow specification of file overwrite policy

    Sets 'parsed_args.overwrite' or 'parsed_args.sync'
    """
    def extend_parser(self, parser):
        syncmode = parser.add_mutually_exclusive_group(required=False)
        syncmode.add_argument('--force',
                              dest='overwrite',
                              action='store_true',
                              help='Always overwrite existing files')
        syncmode.add_argument(
            '--sync',
            dest='sync',
            action='store_true',
            help='Overwrite files only when timestamp or size differs')
        return parser


class ReportProgress(ParserExtender):
    """Configures a Command to report progress to STDERR

    Sets 'parsed_args.progress'
    """
    def extend_parser(self, parser):
        parser.add_argument('--progress',
                            dest='progress',
                            action='store_true',
                            help='Report progress to STDERR')
        return parser
