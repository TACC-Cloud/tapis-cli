import os
from tapis_cli.clients.services.mixins import JobsUUID, FilePath
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from ..files.models import File
from ..files.formatters import FilesFormatOne
from .helpers.sync import download

__all__ = ['JobsOutputsDownload']


class JobsOutputsDownload(FilesFormatOne, JobsUUID, FilePath):
    """Download a jobs output file or directory
    """

    # TODO - add --cwd option to disable creating job folder
    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        parser = FilePath.extend_parser(self, parser)
        parser.add_argument(
            '--cwd',
            dest='use_cwd',
            action='store_true',
            help="Download to '.' instead of a job-specific subdirectory")
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

        # Optionally disable creation and use of a job folder
        dest_dir = './{0}'.format(parsed_args.job_uuid)
        if parsed_args.use_cwd:
            dest_dir = '.'
        else:
            os.path.makedirs(dest_dir, exist_ok=True)

        headers = SearchableCommand.headers(self, File, parsed_args)
        downloaded, skipped, exceptions, elapsed = download(
            file_path=parsed_args.file_path,
            job_uuid=parsed_args.job_uuid,
            destination=dest_dir,
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
