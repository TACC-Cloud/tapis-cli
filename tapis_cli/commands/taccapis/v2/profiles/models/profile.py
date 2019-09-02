"""Data model and functions for Tapis profiles
"""
from .. import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisEntity
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Profile', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'profiles'


class Profile(TapisEntity):
    """Model of a Tapis user profile
    """
    id_display_name = 'USERNAME'
    payload = dict()

    SEARCH_ARGS = [
        # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("first_name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("last_name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("full_name", argtype.STRING, Verbosity.RECORD_VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("email", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("mobile_phone", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("phone", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("username", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("uid", argtype.INTEGER, Verbosity.RECORD_VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("nonce", argtype.STRING, Verbosity.RECORD_VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.RECORD_VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("create_time", argtype.DATETIME, Verbosity.RECORD_VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
    ]

    def __init__(self):
        self.add_fields(self.SEARCH_ARGS)

    def get_headers(self, verbosity_level=None, formatter='table'):
        if verbosity_level is None:
            verbosity_level = Verbosity.LISTING
        headers = list()
        for f in self.fields:
            # print('{}: {}> = {}'.format(f, verbosity_level, f.verbosity))
            if verbosity_level >= f.verbosity:
                if argtype.format_allows_param_type(f, formatter):
                    headers.append(f.param_name)
        return headers
