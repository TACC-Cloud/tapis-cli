"""Public, low-dependency helper functions
"""
from __future__ import print_function
import arrow
import datetime
import fnmatch
import getpass
import importlib
import json
import os
import pkg_resources
import re
import six
import sys
from slugify import slugify as slugifyfn
from requests import get
from requests.exceptions import ConnectTimeout
from socket import getfqdn
from colorama import Fore, Back, Style

from dateutil.parser import parse

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path    # Python 2 backport


def current_time():
    """Current UTC time
    Returns:
        A ``datetime`` object rounded to millisecond precision
    """
    return datetime.datetime.fromtimestamp(
        int(datetime.datetime.utcnow().timestamp() * 1000) / 1000)


def seconds():
    """Current time in seconds as ``int``
    """
    return round(arrow.utcnow().float_timestamp)


def milliseconds():
    """Current time in milliseconds as ``int``
    """
    return round(arrow.utcnow().float_timestamp * 1000)


def microseconds():
    """Current time in microseconds as ``int``
    """
    return round(arrow.utcnow().float_timestamp * 1000 * 1000)


def nanoseconds():
    """Current time in nanoseconds as ``int``
    """
    return round(arrow.utcnow().float_timestamp * 1000 * 1000 * 1000)


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


def datestring_to_epoch(date_string):
    """Convert a date string to UNIX epoch
    """
    return arrow.get(date_string).timestamp


def command_set():
    """Discover and return the full complement of commands
    """
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
    """Generate a string of tab and newline delimited columns from a list
    """
    lines = ("\t".join(mylist[i:i + cols])
             for i in range(0, len(mylist), cols))
    return '\n'.join(lines)


def redact(value):
    return value[0] + ('*' * (len(value) - 2)) + value[-1]


def prompt(body, default=None, secret=False, allow_empty=True):
    """Prompt user for input
    """
    if default is not None:
        if secret is False:
            fdefault = default
        else:
            # Mask out all but first and last two chars of secret value
            fdefault = redact(default)
        qtext = '{0} [{1}]: '.format(body, fdefault)
    else:
        qtext = '{0}: '.format(body)

    try:
        if not secret:
            response = input(qtext)
        else:
            response = getpass.getpass(qtext)
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except Exception:
        raise

    if (response is None or response == '') and default is not None:
        response = default
    else:
        response = response.strip()

    if (response is None or response == '') and allow_empty is False:
        raise ValueError('This value cannot be empty.')
    else:
        return response


def prompt_accept(body, default='y', exit_reject=True):
    if default is None:
        qtext = "{0} (type 'y' or 'n' then Return) ".format(body)
    elif default == 'y':
        qtext = '{0} [Y/n]: '.format(body)
    else:
        qtext = '{0} [y/N]: '.format(body)

    try:
        response = input(qtext).lower()
        if response == '':
            response = default
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except Exception:
        raise

    if isinstance(response, str) and response.startswith('y'):
        return True
    else:
        if exit_reject:
            exit(1)
        else:
            return False


def prompt_boolean(body, default=True):
    if default is True:
        strdef = 'y'
    else:
        strdef = 'n'
    return prompt_accept(body, default=strdef, exit_reject=False)


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


def splitall(path):
    """Splits a path into all of its parts
    """
    # Ref: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:    # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:    # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


# Inspired by https://gist.github.com/moird/3684595
def humanize_bytes(bytesize, precision=2):
    """Render byte counts into human-scale formats
    """
    abbrevs = ((1 << 50, 'PB'), (1 << 40, 'TB'), (1 << 30, 'GB'),
               (1 << 20, 'MB'), (1 << 10, 'kB'), (1, 'bytes'))
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)


def print_stderr(message):
    """Print to STDERR without using logging
    """
    print('{0}'.format(message), file=sys.stderr)


# Color and format text


def fg_red(message):
    """Red text
    """
    return Fore.RED + message + Fore.RESET


def fg_green(message):
    """Green text
    """
    return Fore.GREEN + message + Fore.RESET


def fg_blue(message):
    """Blue text
    """
    return Fore.BLUE + message + Fore.RESET


def fg_bright(message):
    """Bright text
    """
    return Style.BRIGHT + message + Style.RESET_ALL


def fg_dim(message):
    """Dim text
    """
    return Style.DIM + message + Style.RESET_ALL


def fnmatches(file_name, patterns=None):
    """Check if a filename string matches a specified patterns

    Uses UNIX-style file wildcards
    """
    if patterns is None:
        return True
    else:
        for p in patterns:
            if fnmatch.fnmatch(file_name, p):
                return True
        return False


def serializable(obj, permissive=True):
    """Check that a Python object is JSON serializable
    """
    try:
        json.loads(json.dumps(obj))
        return True
    except Exception:
        if permissive:
            return False
        else:
            raise


def timestamp():
    """Returns Zulu-formatted UTC time
    """
    return arrow.utcnow().format('YYMMDDTHHmmss') + 'Z'


def makedirs(file_path, exist_ok=True):
    """Python2-compatible makedirs with exist_ok support
    """
    Path(file_path).mkdir(exist_ok=exist_ok, parents=True)


def dynamic_import(module, package=None):
    """Dynamically import a module by name at runtime

    Args:
        module (str): The name of the module to import
        package (str, optional): The package to import ``module`` from

    Returns:
        object: The imported module
    """
    return importlib.import_module(module, package=package)


def import_submodules(module, package=None, exclude=[]):
    """Dynamically discover and import submodules at runtime
    """
    m = dynamic_import(module, package)
    paths = m.__path__
    real_path = [pt for pt in paths][0]
    submodules = list()
    for c in os.listdir(real_path):
        try:
            if c not in exclude:
                sm = dynamic_import(module + '.' + os.path.basename(c))
                submodules.append(sm)
        except ModuleNotFoundError:
            pass
    return submodules


def parse_uri(url):
    # Agave URI
    if url.startswith('agave://'):
        url = url.replace('agave://', '', 1)
        parts = url.split('/')
        return parts[0], '/' + '/'.join(parts[1:])
    # Agave media URL
    elif url.startswith('https://'):
        url = url.replace('https://', '')
        parts = url.split('/')
        if parts[1] == 'files' and parts[3] == 'media':
            return parts[5], '/'.join(parts[6:])
    else:
        raise InvalidValue('{0} not a valid Agave URL or URI'.format(url))


def num(n):
    try:
        return int(n)
    except ValueError:
        return float(n)


def reserved_environment_vars():
    # TODO - remove this after it is pushed out as part of AgavePy 1.0.0
    return [
        'MSG', '_abaco_Content-Type', '_abaco_execution_id', '_abaco_username',
        '_abaco_actor_state', '_abaco_actor_dbid', '_abaco_actor_id',
        '_abaco_synchronous', '_abaco_jwt_header_name', '_abaco_actor_name',
        '_abaco_access_token'
    ]


def to_slug(inp, lowercase=True):
    """Implements Aloe Slugify.to_slug
    """
    # https://bitbucket.org/tacc-cic/aloe/src/master/aloe-jobslib/src/main/java/edu/utexas/tacc/aloe/jobs/utils/Slug.java
    # Remove single quote characters
    inp = re.sub("'", '', inp)
    # Remove non-ASCII characters
    inp = re.sub(r'[^\x00-\x7F]', '', inp)
    # Whitespace characters reduced to single -
    inp = re.sub('[\s]+', '-', inp)
    inp = re.sub('[^a-zA-Z0-9_]+', '-', inp)
    inp = re.sub('[-]+', '-', inp)
    inp = re.sub('^-', '', inp)
    inp = re.sub('-$', '', inp)
    if lowercase:
        inp = inp.lower()
    return inp


def split_string(inp, separator=','):
    """Split and de-whitespace delimited string
    """
    els = str(inp).split(separator)
    els = [e.strip() for e in els]
    return els


def nrlist(sequence):
    """Python 2.7 compatible list deduplication
    """
    unique = []
    [unique.append(item) for item in sequence if item not in unique]
    return unique


def slugify(text, separator='_'):
    """Implements a stable slugify function over python-slugify, unicode-slugify, or awesome-slugify
    """
    try:
        # Preferred: python-slugify (https://github.com/un33k/python-slugify)
        # [This usage also works for awesome-slugify (https://github.com/voronind/awesome-slugify)]
        return slugifyfn(text, separator=separator)
    # Thrown when an unexpected keyword argument is encountered
    except TypeError:
        try:
            # Fall back to unicode-slugify (https://github.com/mozilla/unicode-slugify)
            return slugifyfn(text, ok='_-', spaces=False,
                             lower=True).replace('-', separator)
        except Exception:
            raise
    except Exception:
        raise
