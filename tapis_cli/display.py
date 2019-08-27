"""Constants, classes, and helpers pertaining to results display
"""

__all__ = ['Verbosity']


class Verbosity:
    BRIEF = 0
    LISTING = 1
    RECORD = 2
    EXPANDED = 3
    VERBOSE = LISTING
    VERY_VERBOSE = RECORD
    VERY_VERBOSE = EXPANDED
