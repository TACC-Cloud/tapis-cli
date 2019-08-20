import os
import warnings
# from .helpers import (fix_assets_path, array_from_string, parse_boolean,
#                       int_or_none, set_from_string)
from dotenv import load_dotenv, find_dotenv
from dateutil.parser import parse
# from . import constants

BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1')

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    if not load_dotenv(find_dotenv()):
        if not load_dotenv(find_dotenv(usecwd=True)):
            load_dotenv(os.path.join(os.path.expanduser('~'), '.env'))

from .debug import *
from .display import *
from .organization import *

from .abaco import *
from .agave import *
from .aloe import *
from .gitlab import *
from .jupyter import *


def all_settings():
    from types import ModuleType

    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") \
                and not isinstance(item, ModuleType):
            settings[name] = item
    return settings
