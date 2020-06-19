"""Functions supporting redaction of private settings
"""

import re

__all__ = ['key_is_private', 'auto_redact', 'redact']

PRIVATE_TOKENS = ['password', 'token', 'secret']
PRIVATE_RE = re.compile('|'.join(PRIVATE_TOKENS), re.IGNORECASE)
REDACT_CHAR = '*'


def key_is_private(key):
    """Determine if a key has a name indicating it is private
    """
    if PRIVATE_RE.search(key):
        return True
    else:
        return False


def redact(value):
    if value is None:
        return None
    elif len(value) > 1:
        return value[0] + (REDACT_CHAR * (len(value) - 2)) + value[-1]
    else:
        return value


def auto_redact(key, value):
    """Automatically redact values of private settings
    """
    if value is None:
        return None
    else:
        if not key_is_private(key):
            return value
        else:
            return redact(value)
