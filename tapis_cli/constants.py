"""Constant values and help strings
"""

__all__ = [
    'PLATFORM', 'CLI', 'ACCESS_TOKEN', 'REFRESH_TOKEN', 'TENANT', 'CLIENT_KEY',
    'CLIENT_SECRET', 'PEM_TRUE', 'PEM_FALSE'
]

# Platform name (useful if we rebrand)
PLATFORM = 'Tapis'
# CLI top-level command
CLI = 'tapis'
# Bearer token
ACCESS_TOKEN = 'access_token'
# Refresh token
REFRESH_TOKEN = 'refresh_token'
# Tenant concept
TENANT = 'tenant'
# Oauth client key
CLIENT_KEY = 'client key'
# Oauth client secret
CLIENT_SECRET = 'client secret'
# Has permission
PEM_TRUE = 'X'
# Does not have permission
PEM_FALSE = ' '
