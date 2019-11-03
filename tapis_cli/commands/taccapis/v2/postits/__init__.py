"""PostIts service commands
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
API_NAME = 'postits'

from .create import PostItsCreate
from .delete import PostItsDelete
from .list import PostItsList
