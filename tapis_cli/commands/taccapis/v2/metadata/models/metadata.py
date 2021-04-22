"""Data model and functions for Tapis apps
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Metadata', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'meta'


class Metadata(TapisModel):
    """Model of a Tapis metadata record
    """
    service_id_type = 'Unique'

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("uuid", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("schemaId", argtype.STRING, Verbosity.RECORD_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("internalUsername", argtype.STRING, Verbosity.RECORD_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("owner", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("associationIds", argtype.ARRAY, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("value", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("created", argtype.DATETIME, Verbosity.RECORD, argmod.DATE_DEFAULTS,
         argmod.DATE_DEFAULT_MOD, None, None, False),
        ("lastUpdated", argtype.DATETIME, Verbosity.RECORD,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, False),
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
