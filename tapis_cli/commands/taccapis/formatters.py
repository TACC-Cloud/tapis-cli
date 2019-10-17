from tapis_cli.clients.services import taccapis
from tapis_cli.commands.taccapis import SearchableCommand

# import (TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany TaccApisFormatOneNoBearer)

__all__ = [
    'TaccApisCommandBase', 'TaccApisFormatOne', 'TaccApisFormatMany',
    'TaccApisFormatOneNoBearer', 'TaccApisFormatManyUnlimited'
]


class TaccApisCommandBase(taccapis.TaccApisCommandBase, SearchableCommand):
    pass


class TaccApisFormatOne(taccapis.TaccApisFormatOne):
    pass


class TaccApisFormatMany(taccapis.TaccApisFormatMany):
    pass


class TaccApisFormatManyUnlimited(taccapis.TaccApisFormatManyUnlimited):
    pass


class TaccApisFormatOneNoBearer(taccapis.TaccApisFormatOneNoBearer):
    pass
