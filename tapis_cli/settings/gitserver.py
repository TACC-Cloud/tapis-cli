"""Git server settings
"""
import os
from .helpers import (parse_boolean, int_or_none)

__all__ = [
    'TAPIS_CLI_GIT_USERNAME', 'TAPIS_CLI_GIT_TOKEN', 'TAPIS_CLI_GIT_NAMESPACE'
]

# Default to public Github
# TAPIS_CLI_GIT_URL = os.environ.get('TAPIS_CLI_GIT_URL', 'https://github.com')

TAPIS_CLI_GIT_USERNAME = os.environ.get('TAPIS_CLI_GIT_USERNAME', None)
TAPIS_CLI_GIT_TOKEN = os.environ.get('TAPIS_CLI_GIT_TOKEN', None)
# Default to git server username if not specified
TAPIS_CLI_GIT_NAMESPACE = os.environ.get('TAPIS_CLI_GIT_NAMESPACE',
                                         TAPIS_CLI_GIT_USERNAME)
