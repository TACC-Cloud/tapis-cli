"""Constants, classes, and helpers pertaining to results display
"""

__all__ = ['Verbosity', 'abbreviate']

SHORTEN_THRESHOLD = 36


class Verbosity:
    BRIEF = 0
    BRIEF_VERBOSE = 0.5
    LISTING = 1
    LISTING_VERBOSE = 1.5
    RECORD = 2
    RECORD_VERBOSE = 2.5
    EXPANDED = 3
    EXPANDED_VERBOSE = EXPANDED
    VERBOSE = LISTING
    VERY_VERBOSE = RECORD
    VERY_VERBOSE = EXPANDED


def abbreviate(value):
    str_val = str(value)
    if len(str_val) > SHORTEN_THRESHOLD:
        substr_len = int((SHORTEN_THRESHOLD / 2) - 1)
        # str_val = str_val[0:(SHORTEN_THRESHOLD - 9)] + '...' + str_val[-6:]
        str_val = str_val[0:substr_len] + '..' + str_val[(-1 * substr_len):]
    return str_val
