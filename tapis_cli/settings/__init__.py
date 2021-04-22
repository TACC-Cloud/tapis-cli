"""Provides a consistent environment- and file-driven approach to run-time
application configuration.
"""
import os
from dateutil.parser import parse
from .config import find_config, load_config

_ENV_PATH = load_config()    # noqa

from .redact import auto_redact

from .auth import *
from .gitserver import *
from .jupyter import *
from .organization import *

from .debug import *
from .display import *
from .google import *
from .projects import *
from .registry import *
# from .ssh import *
from .taccapis.v1 import *
from .taccapis.v2 import *


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
    sorted_settings = {
        k: auto_redact(k, v)
        for (k, v) in sorted(settings.items())
    }
    return sorted_settings
