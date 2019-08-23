"""Apps service commands
"""
from .....clients.services.taccapis import (TaccApisBase, TaccApisFormatOne,
                                            TaccApisFormatMany)
from .. import SERVICE_VERSION
from .models import App

API_NAME = 'apps'


class AppsBase(TaccApisBase):
    id_display_name = App.id_display_name


class AppsFormatOne(AppsBase, TaccApisFormatOne):
    pass


class AppsFormatMany(AppsBase, TaccApisFormatMany):
    pass
