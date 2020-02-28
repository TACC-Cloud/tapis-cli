"""Data model and functions for Abaco Nonces
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Actor', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'actors'


class Nonce(TapisModel):
    """Model of a Tapis Actor Nonce
    """
    service_id_type = 'Nonce'
    FILTERABLE_KEYS = ['description', 'level']
    SEARCH_ARGS = [
        ("actorId", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("apiServer", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("createTime", argtype.DATETIME, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("currentUses", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("description", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("lastUseTime", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("level", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("maxUses", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("owner", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("remainingUses", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("roles", argtype.ARRAY, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("_links", argtype.ARRAY, Verbosity.VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
