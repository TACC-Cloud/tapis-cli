import os
from tapis_cli.clients.services.mixins import RemoteFilePath
from tapis_cli.utils import makedirs

from . import API_NAME, SERVICE_VERSION
from .mixins import JobsUUID
from ..files.models import File
from .formatters import JobsFormatOne
from .helpers.sync import download
from ..files.mixins import ExcludeFiles, IncludeFiles, OverwritePolicy, ReportProgress

__all__ = ['JobsOutputsDownload']


class JobsOutputsDownload(JobsFormatOne, JobsUUID, RemoteFilePath,
                          ExcludeFiles, IncludeFiles, OverwritePolicy,
                          ReportProgress):

    HELP_STRING = 'Download outputs from a Job'
    LEGACY_COMMMAND_STRING = 'jobs-output-get'

    # TODO - add --cwd option to disable creating job folder
    def get_parser(self, prog_name):
        parser = super(JobsOutputsDownload, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        parser = RemoteFilePath.extend_parser(self, parser)
        parser = OverwritePolicy.extend_parser(self, parser)
        # parser = IncludeFiles.extend_parser(self, parser)
        parser = ExcludeFiles.extend_parser(self, parser)
        parser = ReportProgress.extend_parser(self, parser)
        parser.add_argument(
            '--cwd',
            dest='use_cwd',
            action='store_true',
            help="Download to '.' instead of a job-specific subdirectory")
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)

        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        # Optionally disable creation and use of a job folder
        dest_dir = './{0}'.format(identifier)
        if parsed_args.use_cwd:
            dest_dir = '.'
        else:
            makedirs(dest_dir, exist_ok=True)

        headers = self.render_headers(File, parsed_args)
        downloaded, skipped, exceptions, elapsed = download(
            parsed_args.file_path,
            identifier,
            destination=dest_dir,
            excludes=parsed_args.exclude_files,
        # includes=parsed_args.include_files,
            force=parsed_args.overwrite,
            sync=parsed_args.sync,
            progress=parsed_args.progress,
            atomic=False,
            agave=self.tapis_client)

        headers = ['downloaded', 'skipped', 'messages', 'elapsed_sec']
        if parsed_args.formatter in ('json', 'yaml'):
            data = [downloaded, skipped, [str(e) for e in exceptions], elapsed]
        else:
            data = [len(downloaded), len(skipped), len(exceptions), elapsed]
        return (tuple(headers), tuple(data))
