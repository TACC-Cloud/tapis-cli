"""Data model and functions for Tapis systems
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['System', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'systems'


class System(TapisModel):
    """Model of a Tapis system
    """
    service_id_type = 'System'
    ARGS_ORDERED = ['id', 'name', 'type', 'default']
    # WARNING - date search apparently does not work on systems so never make datetime fields searchable
    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False),
        ("available", argtype.BOOLEAN, Verbosity.LISTING, argmod.BOOL_DEFAULTS,
         argmod.BOOL_DEFAULT_MOD, None, None, True),
        ("default", argtype.BOOLEAN, Verbosity.BRIEF, argmod.BOOL_DEFAULTS,
         argmod.BOOL_DEFAULT_MOD, None, None, True),
        ("description", argtype.STRING, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("environment", argtype.OBJECT, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("executionType", argtype.STRING, Verbosity.RECORD, argmod.DEFAULTS,
         argmod.DEFAULT, ['HPC', 'CLI', 'Condor'], None, True),
        ("globalDefault", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.BOOL_DEFAULTS, argmod.BOOL_DEFAULT_MOD, None, None, True),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("lastModified", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, False),
        ("login", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("maxSystemJobs", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("maxSystemJobsPerUser", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("owner", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("public", argtype.BOOLEAN, Verbosity.LISTING, argmod.BOOL_DEFAULTS,
         argmod.BOOL_DEFAULT_MOD, None, None, True),
        ("queues", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("revision", argtype.INTEGER, Verbosity.RECORD, argmod.NUMBER_DEFAULTS,
         argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("scheduler", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT,
         ['CONDOR', 'SGE', 'LSF', 'PBS', 'SLURM', 'CUSTOM_SLURM',
          'FORK'], None, True),
        ("scratchDir", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("site", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.LISTING, argmod.DEFAULTS,
         argmod.DEFAULT, ['UP', 'DOWN', 'MAINTENANCE', 'UNKNOWN'], None, True),
        ("storage", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("type", argtype.STRING, Verbosity.BRIEF, argmod.DEFAULTS,
         argmod.DEFAULT, ['STORAGE', 'EXECUTION'], None, True),
        ("uuid", argtype.STRING, Verbosity.RECORD, argmod.DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("workDir", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False)
    ]
