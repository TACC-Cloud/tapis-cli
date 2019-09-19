"""Provides a consistent environment- and file-driven approach to run-time
application configuration.
"""
import os
import warnings
from dotenv import load_dotenv, find_dotenv
from dateutil.parser import parse

ENV_PREFIX = 'TAPIS_CLI'

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    if not load_dotenv(find_dotenv()):
        if not load_dotenv(find_dotenv(usecwd=True)):
            load_dotenv(os.path.join(os.path.expanduser('~'), '.env'))

from .auth import *
from .debug import *
from .display import *
from .organization import *

from .taccapis.v1 import *
from .taccapis.v2 import *
from .gitlab import *
from .jupyter import *


def all_settings():
    """Returns name and value of all properties resembling settings
    """
    from types import ModuleType

    settings = {}
    for name, item in globals().items():
        # Ignore callables and private properties
        if not callable(item) and not name.startswith("__") \
                and not isinstance(item, ModuleType):
            settings[name] = item
    return settings
