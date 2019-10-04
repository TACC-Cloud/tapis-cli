import os
from .helpers import (ns_os_environ_get, parse_boolean, int_or_none)

__all__ = [
    'DATE_FORMAT', 'LOG_LEVEL', 'PAGE_SIZE', 'RESPONSE_FORMAT', 'FIT_WIDTH',
    'SHOW_CURL'
]

DATE_FORMAT = ns_os_environ_get('DATE_FORMAT', 'YYYYMMDDTHHmmssZZ')
PAGE_SIZE = int_or_none(ns_os_environ_get('PAGE_SIZE', '100'))
LOG_LEVEL = ns_os_environ_get('LOG_LEVEL', None)
RESPONSE_FORMAT = ns_os_environ_get('RESPONSE_FORMAT', None)
FIT_WIDTH = parse_boolean(ns_os_environ_get('FIT_WIDTH', '1'))
SHOW_CURL = parse_boolean(
    ns_os_environ_get('SHOW_CURL', os.environ.get('TAPIS_PY_SHOW_CURL', '0')))
