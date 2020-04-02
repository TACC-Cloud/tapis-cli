import os
import sys
import tempfile
from tapis_cli.display import Verbosity
from tapis_cli.utils import to_slug

from ..files.models import File
from ..files.formatters import FilesFormatOne
from .helpers.sync import basic_download as download
from .mixins import JobsUUID
from . import API_NAME, SERVICE_VERSION


class JobsOutputsLogs(FilesFormatOne, JobsUUID):

    HELP_STRING = 'Displays logs for a Tapis Job'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsOutputsLogs, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        # fg = parser.add_mutually_exclusive_group()
        parser.add_argument('--stdout',
                            action='store_true',
                            help='Display job STDOUT instead of STDERR')
        # fg.add_argument('--script',
        #                 action='store_true',
        #                 help='Display job script instead of STDERR')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        # get job name
        job_def = self.tapis_client.jobs.get(jobId=identifier)
        job_name = job_def.get('name')
        filename_root = '{0}-{1}'.format(to_slug(job_name), identifier)
        filename_suffix = '.err'
        if parsed_args.stdout:
            filename_suffix = '.out'
        # placeholder
        # elif parsed_args.script:
        #     filename_suffix = '.ipcexe'
        filename = filename_root + filename_suffix

        # tempfile name to hold the downloaded file
        ftemp = tempfile.mkstemp()[1]

        try:
            download(filename, identifier, dest=ftemp, agave=self.tapis_client)
            filepath = ftemp
            # https://stackoverflow.com/questions/26692284/how-to-prevent-brokenpipeerror-when-doing-a-flush-in-python
            with open(filepath) as fp:
                try:
                    for _, line in enumerate(fp):
                        print(line, flush=True)
                    sys.stdout.flush()
                    os.unlink(ftemp)
                    sys.exit(0)
                except BrokenPipeError:
                    devnull = os.open(os.devnull, os.O_WRONLY)
                    os.dup2(devnull, sys.stdout.fileno())
                    sys.exit(1)
        except Exception as err:
            raise
            sys.exit(1)
