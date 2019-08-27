from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .show import JobsShow
from .formatters import JobsFormatOne, JobsFormatMany

__all__ = ['JobsStatus']


class JobsStatus(JobsShow):
    """Show status a specific job record
    """
    VERBOSITY = Verbosity.BRIEF
