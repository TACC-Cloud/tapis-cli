import os
from agavepy.settings import SHOW_CURL as TAPIS_PY_SHOW_CURL
from agavepy.settings import VERBOSE_ERRORS as TAPIS_PY_VERBOSE_ERRORS
from .helpers import (parse_boolean, int_or_none)

__all__ = [
    'TAPIS_CLI_DATE_FORMAT', 'TAPIS_CLI_LOG_LEVEL', 'TAPIS_CLI_PAGE_SIZE',
    'TAPIS_CLI_RESPONSE_FORMAT', 'TAPIS_CLI_FIT_WIDTH', 'TAPIS_CLI_SHOW_CURL',
    'TAPIS_PY_SHOW_CURL', 'TAPIS_CLI_VERBOSE_ERRORS', 'TAPIS_CLI_DISPLAY_AUP',
    'TAPIS_CLI_DISPLAY_COC', 'TAPIS_CLI_SHOW_LEGACY_INTERACTIVE_HELP'
]

TAPIS_CLI_DATE_FORMAT = os.environ.get('TAPIS_CLI_DATE_FORMAT',
                                       'YYYYMMDDTHHmmssZZ')
TAPIS_CLI_PAGE_SIZE = int_or_none(os.environ.get('TAPIS_CLI_PAGE_SIZE', '100'))
TAPIS_CLI_LOG_LEVEL = os.environ.get('TAPIS_CLI_LOG_LEVEL', None)
TAPIS_CLI_RESPONSE_FORMAT = os.environ.get('TAPIS_CLI_RESPONSE_FORMAT',
                                           'table')
TAPIS_CLI_FIT_WIDTH = parse_boolean(os.environ.get('TAPIS_CLI_FIT_WIDTH', '1'))
TAPIS_CLI_SHOW_CURL = parse_boolean(
    os.environ.get('TAPIS_CLI_SHOW_CURL', str(TAPIS_PY_SHOW_CURL)))
TAPIS_CLI_VERBOSE_ERRORS = parse_boolean(
    os.environ.get('TAPIS_CLI_VERBOSE_ERRORS', str(TAPIS_PY_VERBOSE_ERRORS)))
TAPIS_CLI_DISPLAY_AUP = parse_boolean(
    os.environ.get('TAPIS_CLI_DISPLAY_AUP', '1'))
TAPIS_CLI_DISPLAY_COC = parse_boolean(
    os.environ.get('TAPIS_CLI_DISPLAY_COC', '1'))
TAPIS_CLI_SHOW_LEGACY_INTERACTIVE_HELP = parse_boolean(
    os.environ.get('TAPIS_CLI_SHOW_LEGACY_INTERACTIVE_HELP', '0'))
