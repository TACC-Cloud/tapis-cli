"""Formatters customized for App records and listings
"""

from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import App

__all__ = ['AppsFormatOne', 'AppsFormatMany', 'AppsFormatManyUnlimited']


class AppsBase(TaccApisCommandBase):
    pass


class AppsFormatOne(AppsBase, TaccApisFormatOne):
    pass


class AppsFormatMany(AppsBase, TaccApisFormatMany):
    pass


class AppsFormatManyUnlimited(AppsBase, TaccApisFormatManyUnlimited):
    pass
