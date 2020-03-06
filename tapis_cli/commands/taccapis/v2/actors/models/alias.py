"""Data model and functions for Tapis Alias
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Alias']


class Alias(TapisModel):
    service_id_type = 'Alias'
    FILTERABLE_KEYS = ['owner']
    ARGS_ORDERED = ['alias', 'actorId']
    SEARCH_ARGS = [
        ("actorId", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("alias", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("owner", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("_links", argtype.ARRAY, Verbosity.VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
