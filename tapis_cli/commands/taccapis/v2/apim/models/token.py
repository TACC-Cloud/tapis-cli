"""Data model and functions for Tapis token
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Token', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'token'


class Token(TapisModel):
    """Model of a Tapis application
    """
    id_display_name = 'TOKEN'

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("scope", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("token_type", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("expires_at", argtype.DATETIME, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("expires_in", argtype.INTEGER, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("access_token", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("refresh_token", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False)
    ]
