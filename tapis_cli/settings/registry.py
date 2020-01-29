"""Container registry settings
"""
import os
from .helpers import (parse_boolean, int_or_none)

__all__ = [
    'TAPIS_CLI_REGISTRY_URL', 'TAPIS_CLI_REGISTRY_USERNAME',
    'TAPIS_CLI_REGISTRY_PASSWORD', 'TAPIS_CLI_REGISTRY_NAMESPACE'
]

# Default to public Dockerhub
TAPIS_CLI_REGISTRY_URL = os.environ.get('TAPIS_CLI_REGISTRY_URL',
                                        'https://index.docker.io')

TAPIS_CLI_REGISTRY_USERNAME = os.environ.get('TAPIS_CLI_REGISTRY_USERNAME',
                                             None)
TAPIS_CLI_REGISTRY_PASSWORD = os.environ.get('TAPIS_CLI_REGISTRY_PASSWORD',
                                             None)
# Default to container registry username if not specified
TAPIS_CLI_REGISTRY_NAMESPACE = os.environ.get('TAPIS_CLI_REGISTRY_NAMESPACE',
                                              TAPIS_CLI_REGISTRY_USERNAME)
