"""Formatters customized for app records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany)
from .models import App

__all__ = ['AppsFormatOne', 'AppsFormatMany']


class AppsBase(TaccApisBase):
    id_display_name = App.id_display_name


class AppsFormatOne(TaccApisFormatOne, AppsBase):
    pass


class AppsFormatMany(TaccApisFormatMany, AppsBase):
    pass
