import os
from .helpers import parse_boolean

__all__ = ['TENANT_DNS_DOMAIN',
           'TACC_PROJECT_NAME', 'TACC_PROJECT_ID',
           'TACC_TENANT_ID', 'TACC_PROJECT_GROUP',
           'TACC_MANAGER_ACCOUNT', 'TACC_TENANTS_SERVER',
           'TACC_API_SERVER', 'TACC_JUPYTER_SERVER',
           'TACC_PRIMARY_STORAGE_SYSTEM']

TENANT_DNS_DOMAIN = os.environ.get('TENANT_DNS_DOMAIN', 'tacc.utexas.edu')

# TACC.cloud TAS config
# NOTE - These are mocks
TACC_PROJECT_NAME = os.environ.get('TACC_PROJECT_NAME', 'TAPIS_SANDBOX')
TACC_PROJECT_ID = os.environ.get('TACC_PROJECT_ID', '65536')
TACC_PROJECT_GROUP = os.environ.get('TACC_PROJECT_GROUP', '131072')

# TACC.cloud config
TACC_TENANT_ID = os.environ.get('TACC_TENANT', 'tacc.prod')
# NOTE - This is a mock
TACC_MANAGER_ACCOUNT = os.environ.get('TACC_MANAGER_ACCOUNT', 'tacolord')

TACC_TENANTS_SERVER = 'https://api.tacc.utexas.edu/tenants'
TACC_API_SERVER = os.environ.get(
    'TACC_API_SERVER', 'https://api.' + TENANT_DNS_DOMAIN + '/')
TACC_JUPYTER_SERVER = os.environ.get(
    'TACC_JUPYTER_SERVER', 'https://jupyter.' + TENANT_DNS_DOMAIN)

# NOTE - This is a mock
TACC_PRIMARY_STORAGE_SYSTEM = os.environ.get(
    'TACC_PRIMARY_STORAGE_SYSTEM', 'data-tapis-sandbox')
