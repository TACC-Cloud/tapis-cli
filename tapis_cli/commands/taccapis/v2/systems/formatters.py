"""Formatters customized for system records and listings
"""
from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import System

__all__ = ['SystemsFormatOne', 'SystemsFormatMany', 'SystemsHistoryFormatMany']


class SystemsBase(TaccApisCommandBase):
    service_id_type = System.service_id_type


class SystemsFormatOne(SystemsBase, TaccApisFormatOne):
    pass


class SystemsFormatMany(SystemsBase, TaccApisFormatMany):
    pass


class SystemsHistoryFormatMany(SystemsBase, TaccApisFormatMany):
    pass
