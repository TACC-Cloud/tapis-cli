from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import OptionalTapisEntityUUID

from . import API_NAME, SERVICE_VERSION
from .models import Notification
from .formatters import NotificationsFormatMany

__all__ = ['NotificationsList']


class NotificationsList(NotificationsFormatMany, OptionalTapisEntityUUID):

    HELP_STRING = 'List Notifications [by Tapis UUID]'
    LEGACY_COMMMAND_STRING = 'notifications-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING

    def get_parser(self, prog_name):
        parser = super(NotificationsList, self).get_parser(prog_name)
        parser = OptionalTapisEntityUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(Notification, parsed_args)
        if parsed_args.identifier is None:
            results = self.tapis_client.notifications.list(
                limit=parsed_args.limit, offset=parsed_args.offset)
        else:
            results = self.tapis_client.notifications.list(
                associatedUuid=parsed_args.identifier,
                limit=parsed_args.limit,
                offset=parsed_args.offset)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                key, val = self.render_extended_parser_value(
                    key, val, parsed_args)
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
