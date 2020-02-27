import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string, ns_os_environ_get)
from agavepy.settings import (TAPIS_TENANTS_URL, TAPIS_DEFAULT_TENANT_ID)

__all__ = [
    'TAPIS_TENANTS_URL', 'TAPIS_DEFAULT_TENANT_ID', 'TAPIS_CLI_VERIFY_SSL'
]

TAPIS_CLI_VERIFY_SSL = parse_boolean(
    os.environ.get('TAPIS_CLI_VERIFY_SSL', 'true'))
