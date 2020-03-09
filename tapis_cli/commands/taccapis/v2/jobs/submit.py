from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import UploadJSONTemplate

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne

__all__ = ['JobsSubmit']


class JobsSubmit(JobsFormatOne, UploadJSONTemplate):

    HELP_STRING = 'Submit a new Job'
    LEGACY_COMMMAND_STRING = 'jobs-submit'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsSubmit, self).get_parser(prog_name)
        parser = UploadJSONTemplate.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        headers = self.render_headers(Job, parsed_args)
        rec = self.tapis_client.jobs.submit(body=self.json_file_contents)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
