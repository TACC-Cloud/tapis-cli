import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string, ns_os_environ_get)

__all__ = ['DEBUG_MODE']

DEBUG_MODE = parse_boolean(
    ns_os_environ_get('LOCALONLY', ns_os_environ_get('DEBUG', 'false')))
