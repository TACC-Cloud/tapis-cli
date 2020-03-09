import stringcase
from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.clients.services.mixins import OptionalTapisEntityUUID

from . import API_NAME, SERVICE_VERSION
from .formatters import NotificationsFormatOne
from .mixins import UploadNotificationJson, NotificationOptions
from .models import Notification

__all__ = ['NotificationsCreate']

# TODO - enforce use of create vs update by checking for Notification UUID


class NotificationsCreate(NotificationsFormatOne, NotificationOptions,
                          UploadNotificationJson, OptionalTapisEntityUUID):

    HELP_STRING = 'Create a Notification'
    LEGACY_COMMMAND_STRING = 'notifications-addupdate'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(NotificationsCreate, self).get_parser(prog_name)
        parser = OptionalTapisEntityUUID.extend_parser(self, parser)
        parser = NotificationOptions.extend_parser(self, parser)
        # parser = UploadNotificationJson.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        # self.handle_file_upload(parsed_args)
        tapis_uuid = OptionalTapisEntityUUID.get_identifier(self,
                                                            parsed_args,
                                                            permissive=True)

        # if tapis_uuid is not None and self.json_file_contents != {}:
        #     raise RuntimeError(
        #         'Specifing both <tapis_uuid> and -F options is not supported.')

        # Read in the JSON file then override with per-argument values
        # if self.json_file_contents != {}:
        #     body = self.json_file_contents
        # else:
        body = self.parsed_args_to_body(parsed_args, tapis_uuid)

        headers = self.render_headers(Notification, parsed_args)
        rec = self.tapis_client.notifications.add(body=body)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            key, val = self.render_extended_parser_value(key, val, parsed_args)
            data.append(val)
        return (tuple(headers), tuple(data))
