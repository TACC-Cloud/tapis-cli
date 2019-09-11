"""Formatters customized for app records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany)
from .models import App

__all__ = ['AppsFormatOne', 'AppsFormatMany']


class AppsBase(TaccApisCommandBase):
    service_id_type = App.service_id_type


class AppsFormatOne(AppsBase, TaccApisFormatOne):
    pass


class AppsFormatMany(AppsBase, TaccApisFormatMany):
    pass
