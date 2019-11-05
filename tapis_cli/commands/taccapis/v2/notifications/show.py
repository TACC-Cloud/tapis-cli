from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import NotificationsUUID

from . import API_NAME, SERVICE_VERSION
from .models import Notification
from .formatters import NotificationsFormatOne

__all__ = ['NotificationsShow']


class NotificationsShow(NotificationsFormatOne, NotificationsUUID):
    """Show a Notification by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(NotificationsShow, self).get_parser(prog_name)
        parser = NotificationsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.validate_identifier(parsed_args.identifier)

        headers = self.render_headers(Notification, parsed_args)
        results = self.tapis_client.notifications.get(
            uuid=parsed_args.identifier)

        data = []
        for key in headers:
            val = self.render_value(results.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
