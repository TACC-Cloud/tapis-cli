from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne
from .mixins import JobsUUID

__all__ = ['JobsResubmit']


class JobsResubmit(JobsFormatOne, JobsUUID):

    HELP_STRING = 'Resubmit a Job using the same inputs and parameters'
    LEGACY_COMMMAND_STRING = 'jobs-resubmit'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsResubmit, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)

        API_PATH = '{0}/resubmit'.format(identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)

        headers = self.render_headers(Job, parsed_args)
        rec = self.requests_client.post(content_type='application/json')

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
