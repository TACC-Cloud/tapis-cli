from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import UploadJsonFile, NotificationsUUID
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Notification
from .formatters import NotificationsFormatOne

__all__ = ['NotificationsUpdate']

# TODO - enforce use of create vs update by checking for Notification UUID


class NotificationsUpdate(NotificationsFormatOne, UploadJsonFile,
                          NotificationsUUID):
    """Update a Notification by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(NotificationsUpdate, self).get_parser(prog_name)
        parser = NotificationsUUID.extend_parser(self, parser)
        parser = UploadJsonFile.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        headers = self.render_headers(Notification, parsed_args)
        rec = self.tapis_client.notifications.add(body=self.json_file_contents)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
