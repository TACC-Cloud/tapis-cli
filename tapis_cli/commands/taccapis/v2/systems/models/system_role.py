from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from .system import System

__all__ = ['SystemRole']


class SystemRole(System):
    """Model of a Tapis system role
    """
    NAMES = ['GUEST', 'USER', 'PUBLISHER', 'ADMIN', 'OWNER']

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("username", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("role", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True)
    ]
