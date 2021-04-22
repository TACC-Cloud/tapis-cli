from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from .job import Job

__all__ = ['JobPermission']


class JobPermission(Job):

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("username", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("internalUsername", argtype.DATETIME, Verbosity.EXPANDED,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("permission", argtype.OBJECT, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False)
    ]
