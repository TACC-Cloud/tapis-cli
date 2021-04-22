"""Data model and functions for Tapis profiles
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Profile', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'profiles'


class Profile(TapisModel):
    """Model of a Tapis user profile
    """
    service_id_type = 'User'

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("first_name", argtype.STRING, Verbosity.BRIEF, [argmod.EQUALS],
         argmod.DEFAULT, None, None, True),
        ("last_name", argtype.STRING, Verbosity.BRIEF, [argmod.EQUALS],
         argmod.DEFAULT, None, None, True),
        ("full_name", argtype.STRING, Verbosity.RECORD_VERBOSE,
         [argmod.EQUALS], argmod.DEFAULT, None, None, False),
        ("email", argtype.STRING, Verbosity.BRIEF, [argmod.EQUALS],
         argmod.DEFAULT, None, None, True),
        ("mobile_phone", argtype.STRING, Verbosity.RECORD, [argmod.EQUALS],
         argmod.DEFAULT, None, None, False),
        ("phone", argtype.STRING, Verbosity.RECORD, [argmod.EQUALS],
         argmod.DEFAULT, None, None, False),
        ("username", argtype.STRING, Verbosity.BRIEF, [argmod.EQUALS],
         argmod.DEFAULT, None, None, True),
        ("uid", argtype.INTEGER, Verbosity.RECORD_VERBOSE, [argmod.EQUALS],
         argmod.DEFAULT, None, None, False),
        ("nonce", argtype.STRING, Verbosity.RECORD_VERBOSE, [argmod.EQUALS],
         argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.RECORD_VERBOSE, [argmod.EQUALS],
         argmod.DEFAULT, None, None, False),
        ("create_time", argtype.DATETIME, Verbosity.RECORD_VERBOSE,
         [argmod.EQUALS], argmod.DEFAULT, None, None, False),
    ]
