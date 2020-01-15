"""Formatters customized for Actor records and listings
"""

from tapis_cli.commands.taccapis.formatters import (TaccApisCommandBase,
                                                    TaccApisFormatOne,
                                                    TaccApisFormatMany)
from .models import Actor

__all__ = ['ActorsFormatOne', 'ActorsFormatMany']


class ActorsBase(TaccApisCommandBase):
    pass


class ActorsFormatOne(ActorsBase, TaccApisFormatOne):
    pass


class ActorsFormatMany(ActorsBase, TaccApisFormatMany):
    pass
