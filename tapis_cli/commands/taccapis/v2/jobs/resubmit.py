from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne

__all__ = ['JobsResubmit']


class JobsResubmit(JobsFormatOne, ServiceIdentifier):
    """Resubmit a job using the same inputs and parameters
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = JobsFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = JobsFormatOne.before_take_action(self, parsed_args)
        API_PATH = '{0}/resubmit'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)

        headers = SearchableCommand.headers(self, Job, parsed_args)
        rec = self.requests_client.post(content_type='application/json')

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
