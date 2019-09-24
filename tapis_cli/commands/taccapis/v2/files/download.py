import os
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier, AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import File
from .formatters import FilesFormatOne
from .helpers.sync import download

__all__ = ['FilesDownload']


class FilesDownload(FilesFormatOne, AgaveURI):
    """Download a file or directory to local host
    """

    # TODO - add formatting and sorting options
    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser.add_argument('--exclude',
                            nargs='+',
                            metavar='filename',
                            help='One or more files to exclude from download')
        syncmode = parser.add_mutually_exclusive_group(required=False)
        syncmode.add_argument('--force',
                              dest='overwrite',
                              action='store_true',
                              help='Always overwrite existing files')
        syncmode.add_argument(
            '--sync',
            dest='sync',
            action='store_true',
            help='Overwrite only when timestamp or size differs')
        # parser.add_argument('--atomic',
        #                     dest='atomic',
        #                     action='store_true',
        #                     help='Download atomically')
        parser.add_argument('--progress',
                            dest='progress',
                            action='store_true',
                            help='Report progress to STDERR')

        # TODO - options (force, atomic, sync, parallel, etc)
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatOne.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, File, parsed_args)
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        downloaded, skipped, exceptions, elapsed = download(
            file_path,
            storage_system,
            destination='.',
            excludes=parsed_args.exclude,
            force=parsed_args.overwrite,
            sync=parsed_args.sync,
            progress=parsed_args.progress,
            atomic=parsed_args.atomic,
            agave=self.tapis_client)

        headers = ['downloaded', 'skipped', 'errors', 'elapsed_sec']
        if parsed_args.formatter in ('json', 'yaml'):
            data = [downloaded, skipped, [str(e) for e in exceptions], elapsed]
        else:
            data = [len(downloaded), len(skipped), len(exceptions), elapsed]
        return (tuple(headers), tuple(data))
