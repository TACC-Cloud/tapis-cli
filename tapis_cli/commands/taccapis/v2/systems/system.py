"""Data model and functions for Tapis systems
"""
from tapis_cli.commands.taccapis import TapisEntity
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from . import SERVICE_VERSION

__all__ = ['System', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'systems'


class System(TapisEntity):
    """Model of a Tapis system
    """
    id_display_name = 'SYSTEM_ID'
    payload = dict()

    SEARCH_ARGS = [
        # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False),
        ("available", argtype.BOOLEAN, Verbosity.RECORD, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("default", argtype.BOOLEAN, Verbosity.RECORD, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("description", argtype.STRING, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("environment", argtype.OBJECT, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("executionType", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("globalDefault", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.BOOL_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("lastUpdated", argtype.DATETIME, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        # ("lastModified", argtype.DATETIME, Verbosity.BRIEF,
        #  argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("login", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("maxSystemJobs", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("maxSystemJobsPerUser", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("owner", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("public", argtype.BOOLEAN, Verbosity.LISTING, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("queues", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("revision", argtype.INTEGER, Verbosity.RECORD, argmod.NUMBER_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("scheduler", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("scratchDir", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("site", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, ["UP", "DOWN"], None, False),
        ("storage", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("type", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, ["STORAGE", "EXECUTION"], None, False),
        ("uuid", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("workDir", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False)
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
