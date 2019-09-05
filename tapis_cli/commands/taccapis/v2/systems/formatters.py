"""Formatters customized for system records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from .models import System

__all__ = ['SystemsFormatOne', 'SystemsFormatMany', 'SystemsHistoryFormatMany']


class SystemsBase(TaccApisBase):
    id_display_name = System.id_display_name


class SystemsFormatOne(TaccApisFormatOne, SystemsBase):
    pass


class SystemsFormatMany(TaccApisFormatMany, SystemsBase):
    pass


class SystemsHistoryFormatMany(TaccApisFormatMany, SystemsBase):
    pass
