"""Enumeration of valid types for search arguments
"""
STRING = str
INTEGER = int
FLOAT = float
DOUBLE = FLOAT
NUMBER = FLOAT
DATETIME = 'datetime'
BOOLEAN = bool
NONE = None
ARRAY = list
OBJECT = dict

DEFAULT = STRING

__all__ = ['param_type_repr', 'format_allows_param_type']


def param_type_repr(param_type):
    if param_type == STRING:
        repr = 'string'
    elif param_type == INTEGER:
        repr = 'int'
    elif param_type in (DOUBLE, FLOAT):
        repr = 'decimal'
    elif param_type == DATETIME:
        repr = 'date_string'
    elif param_type == BOOLEAN:
        repr = 'true|false'
    else:
        repr = ''
    return repr.upper()


def format_allows_param_type(argdef, formatter='table'):
    """Filter (mostly structured) un-formattable arguments

    This method implements a handful fo empirically-determined policies to
    filter out parameter types that cannot be easily displayed in flattened
    formats like 'table' or 'value'.
    """
    if formatter == 'json':
        return True
    elif formatter == 'yaml':
        if argdef.param_type in [OBJECT]:
            return False
        else:
            return True
    elif formatter in ('csv', 'table', 'shell', 'value'):
        if argdef.param_type in [ARRAY, OBJECT]:
            return False
        else:
            return True
    else:
        return True
