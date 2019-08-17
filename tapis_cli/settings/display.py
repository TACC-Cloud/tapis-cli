import os
from .helpers import parse_boolean, int_or_none

__all__ = ['DATE_FORMAT', 'LOG_LEVEL', 'PAGE_SIZE', 'RESPONSE_FORMAT']

DATE_FORMAT = os.environ.get("DATE_FORMAT", "YYYYMMDDTHHmmssZZ")
PAGE_SIZE = int_or_none(os.environ.get("PAGE_SIZE", "100"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", None)
RESPONSE_FORMAT = os.environ.get("RESPONSE_FORMAT", None)
