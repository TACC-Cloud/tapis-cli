import json
from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis.model.v2 import Message
from .mixins import JobsUUID

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne

__all__ = ['JobsCancel']


class JobsCancel(JobsFormatOne, JobsUUID):

    HELP_STRING = 'Cancel a running or queued Job'
    LEGACY_COMMMAND_STRING = 'jobs-stop'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsCancel, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)
        API_PATH = '{0}'.format(identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)

        headers = self.render_headers(Message, parsed_args)
        message, warning = '', ''

        try:
            payload = json.dumps({'action': 'stop'})
            # Expecting a 'message' back from API call
            warning = self.requests_client.post(
                data=payload, content_type='application/json')
            message = 'Cancelled Job {0}'.format(identifier)
        except Exception as exc:
            message = 'Failed to cancel Job {0}'.format(identifier)
            warning = str(exc)

        data = [message, warning]
        return (tuple(headers), tuple(data))
