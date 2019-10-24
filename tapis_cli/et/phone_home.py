from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode, urlunparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import platform
import requests
import six
import sys
from random import randint

from tapis_cli import settings
from tapis_cli.utils import get_hostname
from tapis_cli.constants import GOOGLE_ANALYTICS_ID
from tapis_cli.user_agent import user_agent


def generate_tracking_url(path=None):
    """Generates a Google Analytics tracking URL
    """
    if path is None:
        python_version = '{0}.{1}.{2}'.format(sys.version_info.major,
                                              sys.version_info.minor,
                                              sys.version_info.micro)
        os_version = str(platform.platform())
        visit_path = '/stats/python/{0}/platform/{1}'.format(
            python_version, os_version)
    else:
        visit_path = path

    data = {
        'utmwv':
        '5.2.2d',
        'utmn':
        str(randint(1, 9999999999)),
        'utmp':
        visit_path,
        'utmac':
        GOOGLE_ANALYTICS_ID,
        'utmcc':
        '__utma=%s;' %
        '.'.join(['1', settings.TAPIS_CLI_GA_VISITOR, '1', '1', '1', '1'])
    }

    path_els = ('https', 'www.google-analytics.com', '/__utm.gif', '',
                urlencode(data), '')
    if not six.PY3:
        # Coerce to strings to avoid mixed-type error in urlunparse
        path_els = [str(e) for e in path_els]

    url = urlunparse(path_els)
    return url


def phone_home():
    """Report a usage event to Google Analytics (if not disabled)
    """
    if not settings.TAPIS_CLI_GA_DISABLE:
        try:
            headers = {'user-agent': user_agent()}
            requests.get(generate_tracking_url(), headers=headers)
        except Exception:
            pass
