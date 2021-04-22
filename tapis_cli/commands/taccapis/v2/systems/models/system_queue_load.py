from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from .system import System

__all__ = ['SystemQueueLoad']


class SystemQueueLoad(System):
    """Model of the load on a Tapis system virtual queue
    """
    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("active", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("backlogged", argtype.INTEGER, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("pending", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("paused", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("processingInputs", argtype.INTEGER, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("stagingInputs", argtype.INTEGER, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("staging", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("submitting", argtype.INTEGER, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("queued", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("running", argtype.INTEGER, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("cleaningUp", argtype.INTEGER, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("archiving", argtype.INTEGER, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False)
    ]
