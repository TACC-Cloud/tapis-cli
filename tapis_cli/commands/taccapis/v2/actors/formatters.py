"""Formatters customized for Actor records and listings
"""

from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import Actor

__all__ = ['ActorsFormatOne', 'ActorsFormatMany', 'ActorsFormatManyUnlimited']


class ActorsBase(TaccApisCommandBase):
    ACCEPT_NONCE = False
    pass


class ActorsFormatOne(ActorsBase, TaccApisFormatOne):
    pass


class ActorsFormatMany(ActorsBase, TaccApisFormatMany):
    pass


class ActorsFormatManyUnlimited(ActorsBase, TaccApisFormatManyUnlimited):
    pass
