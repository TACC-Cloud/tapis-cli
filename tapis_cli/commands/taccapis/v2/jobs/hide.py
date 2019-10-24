from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import JobsUUID
from tapis_cli.commands.taccapis.model.v2 import Message

from . import API_NAME, SERVICE_VERSION
from .formatters import JobsFormatOne

__all__ = ['JobsHide']


class JobsHide(JobsFormatOne, JobsUUID):
    """Hide a Job from view
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsHide, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.validate_identifier(parsed_args.identifier)

        headers = self.render_headers(Message, parsed_args)
        message, warning = '', ''
        try:
            API_PATH = '{0}/hide'.format(parsed_args.identifier)
            self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
            self.requests_client.post(content_type='application/json')
            message = 'Hid {0}'.format(parsed_args.identifier)
        except Exception as err:
            message = 'Failed to hide {0}'.format(parsed_args.identifier)
            warning = str(err)

        data = [message, warning]
        return (tuple(headers), tuple(data))
