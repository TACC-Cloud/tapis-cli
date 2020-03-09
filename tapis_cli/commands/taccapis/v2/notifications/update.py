import stringcase
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import UploadJsonFile
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.search import spinal_to_camel
from . import API_NAME, SERVICE_VERSION
from .mixins import NotificationsUUID
from .models import Notification
from .create import NotificationsCreate

__all__ = ['NotificationsUpdate']

# TODO - enforce use of create vs update by checking for Notification UUID


class NotificationsUpdate(NotificationsCreate, NotificationsUUID):

    HELP_STRING = 'Update a Notification by UUID'
    LEGACY_COMMMAND_STRING = 'notifications-addupdate'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(NotificationsUpdate, self).get_parser(prog_name)
        parser = NotificationsUUID.extend_parser(self, parser)
        return parser
