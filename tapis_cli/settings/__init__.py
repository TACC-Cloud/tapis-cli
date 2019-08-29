"""Provides a consistent environment- and file-driven approach to run-time
application configuration.
"""
import os
import warnings
# from .helpers import (fix_assets_path, array_from_string, parse_boolean,
#                       int_or_none, set_from_string)
from dotenv import load_dotenv, find_dotenv
from dateutil.parser import parse
# from . import constants

ENV_PREFIX = 'TAPIS_CLI'

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    if not load_dotenv(find_dotenv()):
        if not load_dotenv(find_dotenv(usecwd=True)):
            load_dotenv(os.path.join(os.path.expanduser('~'), '.env'))

from .debug import *
from .display import *
from .organization import *

from .taccapis.v1 import *
from .taccapis.v2 import *


def all_settings():
    from types import ModuleType

    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") \
                and not isinstance(item, ModuleType):
            settings[name] = item
    return settings
