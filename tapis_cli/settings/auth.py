import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string, ns_os_environ_get)
from agavepy.settings import (TAPIS_TENANTS_URL, TAPIS_DEFAULT_TENANT_ID,
                              TAPISPY_VERIFY_SSL)

__all__ = [
    'TAPIS_TENANTS_URL', 'TAPIS_DEFAULT_TENANT_ID', 'TAPIS_CLI_VERIFY_SSL',
    'TAPIS_CLI_WARN_INSECURE_SSL'
]

# Whether Tapis API calls should verify SSL certificates. Inherits default
# from current TapisPy setting. Depends on agavepy==1.0.0a9
TAPIS_CLI_VERIFY_SSL = parse_boolean(
    os.environ.get('TAPIS_CLI_VERIFY_SSL', TAPISPY_VERIFY_SSL))

# Disable InsecureRequestWarning
TAPIS_CLI_WARN_INSECURE_SSL = parse_boolean(
    os.environ.get('TAPIS_CLI_WARN_INSECURE_SSL', False))
if not TAPIS_CLI_WARN_INSECURE_SSL:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
