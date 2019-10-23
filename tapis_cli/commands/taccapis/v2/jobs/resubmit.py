from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import JobsUUID

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne

__all__ = ['JobsResubmit']


class JobsResubmit(JobsFormatOne, JobsUUID):
    """Resubmit a Job using the same inputs and parameters
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsResubmit, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        API_PATH = '{0}/resubmit'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)

        headers = self.render_headers(Job, parsed_args)
        rec = self.requests_client.post(content_type='application/json')

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
