"""Notifications service commands
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
API_NAME = 'notifications'

from .create import NotificationsCreate
from .delete import NotificationsDelete
from .list import NotificationsList
from .show import NotificationsShow
# from .update import NotificationsUpdate
