"""Constants, classes, and helpers pertaining to results display
"""

__all__ = ['Verbosity']


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
