from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis.model.v2 import Message

from . import API_NAME, SERVICE_VERSION
from .formatters import JobsFormatOne
from .mixins import JobsUUID

__all__ = ['JobsHide']


class JobsHide(JobsFormatOne, JobsUUID):

    HELP_STRING = 'Hide a Job from view'
    LEGACY_COMMMAND_STRING = 'jobs-hide'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsHide, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        headers = self.render_headers(Message, parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)
        message, warning = '', ''
        try:
            API_PATH = '{0}/hide'.format(identifier)
            self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
            self.requests_client.post(content_type='application/json')
            message = 'Hid {0}'.format(identifier)
        except Exception as err:
            message = 'Failed to hide {0}'.format(identifier)
            warning = str(err)

        data = [message, warning]
        return (tuple(headers), tuple(data))
