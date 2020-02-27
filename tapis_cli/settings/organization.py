import os
from .helpers import (parse_boolean, ns_os_environ_get)

__all__ = [
    'TAPIS_CLI_PREF_EXECUTION_SYSTEM', 'TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM',
    'TAPIS_CLI_PREF_STORAGE_SYSTEM'
]

# TENANT_DNS_DOMAIN = os.environ.get('TENANT_DNS_DOMAIN', 'tacc.utexas.edu')

# TACC.cloud TAS config
# NOTE - These are mocks
# TENANT_PROJECT_NAME = os.environ.get('TENANT_PROJECT_NAME', 'TAPIS_SANDBOX')
# TACC_PROJECT_ID = os.environ.get('TACC_PROJECT_ID', '65536')
# TACC_PROJECT_GROUP = os.environ.get('TACC_PROJECT_GROUP', '131072')

# TACC.cloud config
# TACC_TENANT_ID = os.environ.get('TACC_TENANT', 'tacc.prod')
# NOTE - This is a mock
# TACC_MANAGER_ACCOUNT = os.environ.get('TACC_MANAGER_ACCOUNT', 'tacolord')

# TENANT_API_SERVER = os.environ.get('TENANT_API_SERVER',
#                                    'https://api.' + TENANT_DNS_DOMAIN + '/')

# # NOTE - This is a mock
# TENANT_PRIMARY_STORAGE_SYSTEM = os.environ.get('TENANT_PRIMARY_STORAGE_SYSTEM',
#                                                'data-tapis-sandbox')

TAPIS_CLI_PREF_EXECUTION_SYSTEM = os.environ.get(
    'TAPIS_CLI_PREF_EXECUTION_SYSTEM', None)
TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM = os.environ.get(
    'TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM', None)
TAPIS_CLI_PREF_STORAGE_SYSTEM = os.environ.get(
    'TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM', TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM)
