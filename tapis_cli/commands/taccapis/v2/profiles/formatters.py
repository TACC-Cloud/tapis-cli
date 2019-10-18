"""Formatters customized for profile records and listings
"""
from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import Profile

__all__ = ['ProfilesFormatOne', 'ProfilesFormatMany']


class ProfilesBase(TaccApisCommandBase):
    service_id_type = Profile.service_id_type


class ProfilesFormatOne(ProfilesBase, TaccApisFormatOne):
    pass


class ProfilesFormatMany(ProfilesBase, TaccApisFormatManyUnlimited):
    pass
