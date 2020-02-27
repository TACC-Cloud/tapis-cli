"""Project configuration and build settings
"""
import os
from .helpers import (parse_boolean, int_or_none)

__all__ = [
    'TAPIS_CLI_PROJECT_GIT_INIT', 'TAPIS_CLI_PROJECT_GIT_FIRST_COMMIT',
    'TAPIS_CLI_PROJECT_GIT_CREATE_REMOTE'
]

# Automatically init a project as a git repo
TAPIS_CLI_PROJECT_GIT_INIT = parse_boolean(
    os.environ.get('TAPIS_CLI_PROJECT_GIT_INIT', 'true'))

# Automatically commit initial files
#
# Defaults to TAPIS_CLI_PROJECT_GIT_INIT
TAPIS_CLI_PROJECT_GIT_FIRST_COMMIT = parse_boolean(
    os.environ.get('TAPIS_CLI_PROJECT_GIT_FIRST_COMMIT', 'false'))

# Automatically create a remote for the repo
# assuming git server and credentials are available
TAPIS_CLI_PROJECT_GIT_CREATE_REMOTE = parse_boolean(
    os.environ.get('TAPIS_CLI_PROJECT_GIT_CREATE_REMOTE', 'false'))
