"""Data model and functions for Tapis apps
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = [
    'PostIt', 'HTTP_METHODS', 'DEFAULT_MAX_USES', 'DEFAULT_LIFETIME',
    'API_NAME', 'SERVICE_VERSION'
]

API_NAME = 'postits'

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
DEFAULT_LIFETIME = 2592000
DEFAULT_MAX_USES = -1


class PostIt(TapisModel):
    """Model of a Tapis post-it entry
    """
    service_id_type = 'Post-it'

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("postit", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("remainingUses", argtype.INTEGER, Verbosity.BRIEF,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("expires", argtype.DATETIME, Verbosity.BRIEF, argmod.DATE_DEFAULTS,
         argmod.DATE_DEFAULT_MOD, None, None, False),
        ("url", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("creator", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("created", argtype.DATETIME, Verbosity.RECORD, argmod.DATE_DEFAULTS,
         argmod.DATE_DEFAULT_MOD, None, None, False),
        ("noauth", argtype.BOOLEAN, Verbosity.RECORD, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("method", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
