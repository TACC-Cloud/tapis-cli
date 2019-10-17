from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import UploadJsonFile
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne

__all__ = ['JobsSubmit']


class JobsSubmit(UploadJsonFile, JobsFormatOne):
    """Submit a new compute Job
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = JobsFormatOne.get_parser(self, prog_name)
        parser = UploadJsonFile.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = JobsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        headers = SearchableCommand.render_headers(self, Job, parsed_args)
        rec = self.tapis_client.jobs.submit(body=self.json_file_contents)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
