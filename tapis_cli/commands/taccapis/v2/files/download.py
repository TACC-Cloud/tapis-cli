import os
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier, AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.utils import humanize_bytes

from . import API_NAME, SERVICE_VERSION
from .models import File
from .formatters import FilesFormatOne
from .helpers.sync import download
from .mixins import ExcludeFiles, FilesCallbackURI, OverwritePolicy, ReportProgress

__all__ = ['FilesDownload']


class FilesDownload(FilesFormatOne, AgaveURI, ExcludeFiles, OverwritePolicy,
                    ReportProgress):
    """Download a Tapis-managed file or directory to local host
    """

    # TODO - add formatting and sorting options
    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = ExcludeFiles.extend_parser(self, parser)
        parser = OverwritePolicy.extend_parser(self, parser)
        parser = ReportProgress.extend_parser(self, parser)
        # Other options might include:
        # --parallel : whether to attempt parallel downloads
        # --retries : max retries before error
        # --timeout : max elapsed time before error
        # --destination : explicitly specify download destination
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = SearchableCommand.render_headers(self, File, parsed_args)
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        downloaded, skipped, exceptions, dl_bytes, elapsed = download(
            file_path,
            storage_system,
            destination='.',
            excludes=parsed_args.exclude_files,
            force=parsed_args.overwrite,
            sync=parsed_args.sync,
            progress=parsed_args.progress,
            atomic=False,
            agave=self.tapis_client)

        headers = ['downloaded', 'skipped', 'warnings', 'data', 'elapsed_sec']
        if parsed_args.formatter in ('json', 'yaml'):
            data = [
                downloaded, skipped, [str(e) for e in exceptions], dl_bytes,
                elapsed
            ]
        else:
            data = [
                len(downloaded),
                len(skipped),
                len(exceptions),
                humanize_bytes(dl_bytes), elapsed
            ]
        return (tuple(headers), tuple(data))
