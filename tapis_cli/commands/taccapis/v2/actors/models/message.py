"""Data model and functions for Tapis Message
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Message']


class Message(TapisModel):

    service_id_type = 'Message'

    SEARCH_ARGS = [
        ("executionId", argtype.STRING, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("msg", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("_links", argtype.ARRAY, Verbosity.VERBOSE, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]
