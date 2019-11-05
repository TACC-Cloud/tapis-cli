from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import NotificationsUUID

from . import API_NAME, SERVICE_VERSION
from .models import Notification
from .formatters import NotificationsFormatOne

__all__ = ['NotificationsDelete']


class NotificationsDelete(NotificationsFormatOne, NotificationsUUID):
    """Delete a Notification by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(NotificationsDelete, self).get_parser(prog_name)
        parser = NotificationsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.validate_identifier(parsed_args.identifier)

        headers = ['deleted', 'messages']
        deleted = []
        messages = []

        try:
            self.requests_client.delete(parsed_args.identifier)
            deleted.append(parsed_args.identifier)
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]
        return (tuple(headers), tuple(data))
