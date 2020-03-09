import os
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier, AgaveURI
from tapis_cli.utils import print_stderr, seconds, milliseconds

from . import API_NAME, SERVICE_VERSION
from .models import File
from .formatters import FilesFormatOne
from .mixins import FileOptions, ReportProgress
from .helpers.manage import delete

__all__ = ['FilesDelete']


class FilesDelete(FilesFormatOne, AgaveURI, FileOptions, ReportProgress):

    HELP_STRING = 'Delete a file or directory from Tapis'
    LEGACY_COMMMAND_STRING = 'files-delete'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    # TODO - add formatting and sorting options
    def get_parser(self, prog_name):
        parser = super(FilesDelete, self).get_parser(prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = FileOptions.extend_parser(self, parser)
        parser = ReportProgress.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        (storage_system, file_path) = self.parse_url(parsed_args.agave_uri)

        headers = ['deleted', 'skipped', 'warnings', 'elapsed_msec']
        (deleted, skipped, warnings, elapsed) = [[], [], [], 0]

        try:
            start_time = milliseconds()
            delete(file_path, storage_system, agave=self.tapis_client)
            deleted.append(file_path)
            elapsed = milliseconds() - start_time
            if parsed_args.progress:
                print_stderr('Deleted {0}'.format(parsed_args.agave_uri))
        except Exception as exc:
            skipped.append(file_path)
            warnings.append(exc)

        if parsed_args.formatter in ('json', 'yaml'):
            data = [deleted, skipped, [str(w) for w in warnings], elapsed]
        else:
            data = [len(deleted), len(skipped), len(warnings), elapsed]
        return (tuple(headers), tuple(data))
