import os
from .helpers import (parse_boolean, int_or_none)

__all__ = ['TAPIS_CLI_PREFERRED_SSH_KEY', 'TAPIS_CLI_PREFERRED_PUBLIC_KEY']

TAPIS_CLI_PREFERRED_PRIVATE_KEY = os.environ.get(
    'TAPIS_CLI_PREFERRED_PRIVATE_KEY', '~/.ssh/id_rsa')

TAPIS_CLI_PREFERRED_PUBLIC_KEY = os.environ.get(
    'TAPIS_CLI_PREFERRED_PUBLIC_KEY', '~/.ssh/id_rsa.pub')
