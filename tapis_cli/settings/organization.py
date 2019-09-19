import os
from .helpers import (parse_boolean, ns_os_environ_get)

__all__ = [
    'TENANT_DNS_DOMAIN', 'TENANT_PROJECT_NAME', 'TENANT_API_SERVER',
    'TENANT_PRIMARY_STORAGE_SYSTEM'
]

TENANT_DNS_DOMAIN = os.environ.get('TENANT_DNS_DOMAIN', 'tacc.utexas.edu')

# TACC.cloud TAS config
# NOTE - These are mocks
TENANT_PROJECT_NAME = os.environ.get('TENANT_PROJECT_NAME', 'TAPIS_SANDBOX')
# TACC_PROJECT_ID = os.environ.get('TACC_PROJECT_ID', '65536')
# TACC_PROJECT_GROUP = os.environ.get('TACC_PROJECT_GROUP', '131072')

# TACC.cloud config
# TACC_TENANT_ID = os.environ.get('TACC_TENANT', 'tacc.prod')
# NOTE - This is a mock
# TACC_MANAGER_ACCOUNT = os.environ.get('TACC_MANAGER_ACCOUNT', 'tacolord')

TENANT_API_SERVER = os.environ.get('TENANT_API_SERVER',
                                   'https://api.' + TENANT_DNS_DOMAIN + '/')

# NOTE - This is a mock
TENANT_PRIMARY_STORAGE_SYSTEM = os.environ.get('TENANT_PRIMARY_STORAGE_SYSTEM',
                                               'data-tapis-sandbox')
