from tapis_cli.display import Verbosity

from .formatters import NotificationsFormatOne
from .mixins import NotificationsUUID
from .models import Notification
from . import API_NAME, SERVICE_VERSION

__all__ = ['NotificationsDelete']


class NotificationsDelete(NotificationsFormatOne, NotificationsUUID):

    HELP_STRING = 'Delete a Notification'
    LEGACY_COMMMAND_STRING = 'notifications-delete'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(NotificationsDelete, self).get_parser(prog_name)
        parser = NotificationsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        identifier = NotificationsUUID.get_identifier(self, parsed_args)

        headers = ['deleted', 'messages']
        deleted = []
        messages = []

        try:
            self.requests_client.delete(identifier)
            deleted.append(identifier)
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]
        return (tuple(headers), tuple(data))
