"""Formatters customized for profile records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from .models import Profile

__all__ = ['ProfilesFormatOne', 'ProfilesFormatMany']


class ProfilesBase(TaccApisBase):
    id_display_name = Profile.id_display_name


class ProfilesFormatOne(TaccApisFormatOne, ProfilesBase):
    pass


class ProfilesFormatMany(TaccApisFormatManyUnlimited, ProfilesBase):
    pass
