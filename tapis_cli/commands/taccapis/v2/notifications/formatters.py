"""Formatters customized for notification records and listings
"""
from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from tapis_cli.display import Verbosity, abbreviate
from .models import Notification

__all__ = ['NotificationsFormatOne', 'NotificationsFormatMany']


class NotificationsBase(TaccApisCommandBase):
    pass


class NotificationsFormatOne(NotificationsBase, TaccApisFormatOne):
    pass


class NotificationsFormatMany(NotificationsBase, TaccApisFormatMany):
    def render_extended_parser_value(self, key, value, formatter=None):
        key, value = super(NotificationsBase,
                           self).render_extended_parser_value(
                               key, value, formatter=formatter)
        # Shorten long URLs in listing context
        if key == 'url':
            if self.app_verbose_level >= Verbosity.LISTING:
                value = abbreviate(value)
        return key, value
