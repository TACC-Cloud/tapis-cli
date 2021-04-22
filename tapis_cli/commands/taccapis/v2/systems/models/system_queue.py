from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from .system import System

__all__ = ['SystemQueue']


class SystemQueue(System):
    """Model of a Tapis system virtual queue
    """
    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("id", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("mappedName", argtype.STRING, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("description", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("default", argtype.BOOLEAN, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("maxJobs", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("maxUserJobs", argtype.INTEGER, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("maxNodes", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("maxProcessorsPerNode", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("maxMemoryPerNode", argtype.FLOAT, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("maxRequestedTime", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("customDirectives", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("load", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False)
    ]
