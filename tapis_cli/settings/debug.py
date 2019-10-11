import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string, ns_os_environ_get)

__all__ = ['TAPIS_CLI_DEBUG_MODE']

TAPIS_CLI_DEBUG_MODE = parse_boolean(
    os.environ.get('TAPIS_CLI_DEBUG_MODE', 'false'))
