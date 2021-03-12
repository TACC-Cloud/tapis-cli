"""Data model and functions for Tapis Actor
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Actor', 'HTTP_METHODS', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'actors'

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


class Actor(TapisModel):
    """Model of a Tapis actor
    """
    service_id_type = 'Actor'
    FILTERABLE_KEYS = ['name', 'description', 'image', 'owner']
    ARGS_ORDERED = ['id', 'name', 'description', 'owner', 'image']
    SEARCH_ARGS = [
        ("createTime", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("lastUpdateTime", argtype.DATETIME, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("defaultEnvironment", argtype.OBJECT, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("description", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("gid", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("hints", argtype.ARRAY, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("image", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("link", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("mounts", argtype.ARRAY, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("owner", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("privileged", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("queue", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("state", argtype.OBJECT, Verbosity.VERY_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("stateless", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("status", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("statusMessage", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("tasdir", argtype.STRING, Verbosity.VERY_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("token", argtype.BOOLEAN, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("type", argtype.STRING, Verbosity.VERY_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("uid", argtype.INTEGER, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("useContainerUid", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("webhook", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("cronOn", argtype.BOOLEAN, Verbosity.BRIEF, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("cronSchedule", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("cronNextEx", argtype.STRING, Verbosity.RECORD_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("_links", argtype.ARRAY, Verbosity.VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
