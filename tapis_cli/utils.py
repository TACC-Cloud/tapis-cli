"""Public, low-dependency helper functions
"""
import arrow
import datetime
import getpass
import os
import pkg_resources
import re
import six
from requests import get
from requests.exceptions import ConnectTimeout
from socket import getfqdn

from dateutil.parser import parse


def current_time():
    """Current UTC time
    Returns:
        A ``datetime`` object rounded to millisecond precision
    """
    return datetime.datetime.fromtimestamp(
        int(datetime.datetime.utcnow().timestamp() * 1000) / 1000)


def microseconds():
    """Current time in microseconds as ``int``
    """
    return int(round(datetime.datetime.utcnow().timestamp() * 1000 * 1000))


def nanoseconds():
    """Current time in nanoseconds as ``int``
    """
    return int(
        round(datetime.datetime.utcnow().timestamp() * 1000 * 1000 * 1000))


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


def datetime_to_isodate(date_obj):
    """Convert a Python datetime object to ISO-8601
    """
    return arrow.get(date_obj).format('YYYY-MM-DDTHH:mm:ss.SSSZZ')


def datetime_to_human(date_obj):
    """Convert a Python datetime object to a human-friendly string
    """
    return arrow.get(date_obj).humanize()


def command_set():
    FILTERED = ('complete', 'help')
    cset = list()
    epts = pkg_resources.iter_entry_points('tapis.cli')
    for e in epts:
        ename = e.name
        if ename not in FILTERED:
            ename = ename.replace('_', ' ')
        cset.append(ename)
    cset.sort()
    return cset


def fmtcols(mylist, cols):
    lines = ("\t".join(mylist[i:i + cols])
             for i in range(0, len(mylist), cols))
    return '\n'.join(lines)


def prompt(body, default=None, secret=False):
    if default is not None:
        if secret is False:
            fdefault = default
        else:
            # Mask out all but first and last two chars of secret value
            fdefault = default[0:2] + '*' * (len(default) - 2) + default[-3:-1]
        qtext = '{0} [{1}]: '.format(body, fdefault)
    else:
        qtext = '{0}: '.format(body)

    if not secret:
        response = input(qtext)
    else:
        response = getpass.getpass(qtext)

    if (response is None or response == '') and default is not None:
        response = default
    else:
        response = response.strip()
    return response


def get_hostname():
    """Returns the fully-qualified domain name for current localhost
    """
    return getfqdn().lower()


def get_public_ip():
    """Returns localhost's public IP address (or NAT gateway address)
    """
    try:
        ip = get('https://api.ipify.org', timeout=1.0).text
        return ip
    except Exception:
        return '127.0.0.1'


def get_local_username():
    """Returns local system username
    """
    return getpass.getuser()


def normalize(file_path):
    """Trim leading slash or slashes from a path

    Arguments:
        file_path (str): Path to normalize

    Returns:
        str: Normalized file_path
    """
    fp = re.sub('^(/)+', '', file_path)
    fp = re.sub('(/)+$', '', fp)
    return fp


def relpath(file_path, root='/'):
    """Returns path relative to start
    """
    fp = re.sub('^(' + root + ')', '', file_path)
    return fp


def normpath(file_path):
    """Collapse duplicate leading slashes and resolve relative references
    in a path

    Arguments:
        file_path (str): Path to process

    Returns:
        str: Processed file_path
    """
    # Consolidate redundant slashes and relative references
    fp = os.path.normpath(file_path)
    # Tapis filePaths should always be absolute
    if not fp.startswith('/'):
        fp = '/' + fp
    # Strip trailing slash
    fp = re.sub('(/)+$', '', fp)
    return os.path.normpath(fp)


def abspath(file_path, root='/'):
    """Safely combine a relative (which might not actually
    be relative) and base path.

    Arguments:
        file_path (str): Relative path
        root_dir (str, optional): Base path for file_path

    Returns:
        str: Processed file_path
    """
    return os.path.join(root, relpath(file_path))
