from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import JobsUUID

from . import API_NAME, SERVICE_VERSION
from .models import JobHistory
from .formatters import JobsHistoryFormatMany

__all__ = ['JobsHistory']


class JobsHistory(JobsHistoryFormatMany, JobsUUID):
    """List history for a specific job
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsHistory, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.validate_identifier(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(JobHistory, parsed_args)
        results = self.tapis_client.jobs.getHistory(
            jobId=parsed_args.identifier)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
