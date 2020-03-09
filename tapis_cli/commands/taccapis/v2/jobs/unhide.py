from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis.model.v2 import Message

from . import API_NAME, SERVICE_VERSION
from .formatters import JobsFormatOne
from .mixins import JobsUUID

__all__ = ['JobsUnhide']


class JobsUnhide(JobsFormatOne, JobsUUID):

    HELP_STRING = 'Unhide a hidden Job'
    LEGACY_COMMMAND_STRING = 'jobs-unhide'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsUnhide, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)

        headers = self.render_headers(Message, parsed_args)
        message, warning = '', ''
        try:
            API_PATH = '{0}/unhide'.format(identifier)
            self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
            self.requests_client.post(content_type='application/json')
            message = 'Unhid {0}'.format(identifier)
        except Exception as err:
            message = 'Failed to unhide {0}'.format(identifier)
            warning = str(err)

        data = [message, warning]
        return (tuple(headers), tuple(data))
