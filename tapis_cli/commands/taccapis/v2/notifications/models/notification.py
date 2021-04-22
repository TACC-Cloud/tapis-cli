"""Data model and functions for Tapis notifications
"""
import math
from datetime import timedelta
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Notification', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'notifications'


class Notification(TapisModel):
    """Model of a Tapis notification
    """
    service_id_type = 'Notification'

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("associatedUuid", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("event", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("url", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("persistent", argtype.BOOLEAN, Verbosity.LISTING,
         argmod.BOOL_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("responseCode", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("attempts", argtype.INTEGER, Verbosity.RECORD, argmod.NUMBER_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("lastUpdated", argtype.DATETIME, Verbosity.RECORD,
         argmod.DATE_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("created", argtype.DATETIME, Verbosity.RECORD, argmod.DATE_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("policy", argtype.OBJECT, Verbosity.RECORD, argmod.DATE_DEFAULTS,
         argmod.DEFAULT, None, None, True),
    ]
