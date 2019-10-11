import os
from agavepy.settings import SHOW_CURL as TAPIS_PY_SHOW_CURL
from .helpers import (parse_boolean, int_or_none)

__all__ = [
    'TAPIS_CLI_DATE_FORMAT', 'TAPIS_CLI_LOG_LEVEL', 'TAPIS_CLI_PAGE_SIZE',
    'TAPIS_CLI_RESPONSE_FORMAT', 'TAPIS_CLI_FIT_WIDTH', 'TAPIS_CLI_SHOW_CURL',
    'TAPIS_PY_SHOW_CURL'
]

TAPIS_CLI_DATE_FORMAT = os.environ.get('TAPIS_CLI_DATE_FORMAT',
                                       'YYYYMMDDTHHmmssZZ')
TAPIS_CLI_PAGE_SIZE = int_or_none(os.environ.get('TAPIS_CLI_PAGE_SIZE', '100'))
TAPIS_CLI_LOG_LEVEL = os.environ.get('TAPIS_CLI_LOG_LEVEL', None)
TAPIS_CLI_RESPONSE_FORMAT = os.environ.get('TAPIS_CLI_RESPONSE_FORMAT',
                                           'table')
TAPIS_CLI_FIT_WIDTH = parse_boolean(os.environ.get('TAPIS_CLI_FIT_WIDTH', '1'))
TAPIS_CLI_SHOW_CURL = parse_boolean(
    os.environ.get('TAPIS_CLI_SHOW_CURL',
                   os.environ.get('TAPIS_PY_SHOW_CURL', '0')))
