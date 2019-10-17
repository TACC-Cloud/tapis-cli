from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from .models import Job
from . import API_NAME, SERVICE_VERSION
from .formatters import JobsFormatOne

__all__ = ['JobsStatus']


class JobsStatus(JobsFormatOne, ServiceIdentifier):
    """Show the status of a Job
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsStatus, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(Job, parsed_args)
        rec = self.tapis_client.jobs.get(jobId=parsed_args.identifier)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
