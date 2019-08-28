from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .models import System
from .show import SystemsShow

__all__ = ['SystemsStatus']


class SystemsStatus(SystemsShow):
    """Show status of a single system
    """
    VERBOSITY = Verbosity.BRIEF
