import os
import six
from dateutil.parser import parse


def ts_to_isodate(date_string, include_time=False):
    """Convert a datetime string (UTC) into a date string in ISO format"""

    iso_date_str = date_string

    try:
        date = parse(date_string)
        if include_time:
            if six.PY3:
                iso_date_str = date.isoformat(timespec='seconds')
            else:
                iso_date_str = date.isoformat()
        else:
            iso_date_str = date.date().isoformat()
    except ValueError:
        pass

    return iso_date_str


def ts_to_date(date_string):
    """Convert a datetime string (UTC) into a pretty date string"""

    date_rep = date_string

    try:
        date = parse(date_string)
        date_rep = date.strftime('%b %d %H:%M:%S %Y')
    except ValueError:
        pass

    return date_rep
