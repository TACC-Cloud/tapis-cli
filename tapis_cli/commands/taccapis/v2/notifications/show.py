from tapis_cli.display import Verbosity

from .formatters import NotificationsFormatOne
from .mixins import NotificationsUUID
from .models import Notification
from . import API_NAME, SERVICE_VERSION

__all__ = ['NotificationsShow']


class NotificationsShow(NotificationsFormatOne, NotificationsUUID):

    HELP_STRING = 'Show details of a Notification'
    LEGACY_COMMMAND_STRING = 'notifications-list'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(NotificationsShow, self).get_parser(prog_name)
        parser = NotificationsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        identifier = NotificationsUUID.get_identifier(self, parsed_args)

        headers = self.render_headers(Notification, parsed_args)
        results = self.tapis_client.notifications.get(uuid=identifier)

        data = []
        for key in headers:
            val = self.render_value(results.get(key, None))
            key, val = self.render_extended_parser_value(key, val, parsed_args)
            data.append(val)
        return (tuple(headers), tuple(data))
