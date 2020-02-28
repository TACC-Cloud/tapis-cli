"""Data model and functions for Actor workers
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = [
    'Actor', 'HTTP_METHODS', 'API_NAME', 'SERVICE_VERSION', 'FILTERABLE_KEYS'
]

API_NAME = 'actors'

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


class Worker(TapisModel):
    """Model of a Tapis actor Worker
    """
    service_id_type = 'Worker'
    FILTERABLE_KEYS = ['status']
    SEARCH_ARGS = [
        ("chName", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("cid", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("createTime", argtype.DATETIME, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("hostId", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("hostIp", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("image", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("lastExecutionTime", argtype.DATETIME, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("lastHealthCheckTime", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("location", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("tenant", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("_links", argtype.ARRAY, Verbosity.VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
