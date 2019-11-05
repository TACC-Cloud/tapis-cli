"""Formatters customized for notification records and listings
"""
from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import Notification

__all__ = ['NotificationsFormatOne', 'NotificationsFormatMany']


class NotificationsBase(TaccApisCommandBase):
    pass


class NotificationsFormatOne(NotificationsBase, TaccApisFormatOne):
    service_id_type = Notification.service_id_type
    pass


class NotificationsFormatMany(NotificationsBase, TaccApisFormatMany):
    pass
