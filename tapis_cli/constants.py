"""Constant values and help strings
"""

__all__ = [
    'PLATFORM', 'CLI', 'ACCESS_TOKEN', 'REFRESH_TOKEN', 'TENANT', 'CLIENT_KEY',
    'CLIENT_SECRET', 'PEM_TRUE', 'PEM_FALSE', 'GOOGLE_ANALYTICS_ID',
    'TAPIS_AUTH_FAIL', 'API_SERVER', 'TAPIS_AUTH_REJECT', 'NONCE'
]

# Platform name (useful if we rebrand)
PLATFORM = 'Tapis'
# CLI top-level command
CLI = 'tapis'
# Bearer token
ACCESS_TOKEN = 'access token'
# Refresh token
REFRESH_TOKEN = 'refresh token'
# Tenant concept
TENANT = 'tenant'
# Oauth client key
CLIENT_KEY = 'client key'
# Oauth client secret
CLIENT_SECRET = 'client secret'
# API host
API_SERVER = 'API server'

# Has permission
PEM_TRUE = 'True'
# Does not have permission
PEM_FALSE = 'False'

# Google Analytics
GOOGLE_ANALYTICS_ID = 'UA-147552755-1'

# AUTH FAILED
TAPIS_AUTH_FAIL = "Failed to load Tapis API client. Run 'tapis auth init [--interactive]' to resolve this."
TAPIS_AUTH_REJECT = "Unable to authenticate with the provided credentials."

# Abaco-specific access key
NONCE = 'nonce'
