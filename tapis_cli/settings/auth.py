from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string, ns_os_environ_get)

__all__ = ['DEFAULT_TENANT_ID', 'TACC_TENANTS_SERVER']

TACC_TENANTS_SERVER = 'https://api.tacc.utexas.edu/tenants'
DEFAULT_TENANT_ID = ns_os_environ_get('DEFAULT_TENANT_ID', 'tacc.prod')
