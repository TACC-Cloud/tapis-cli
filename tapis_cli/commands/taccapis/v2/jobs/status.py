from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.clients.services.mixins import ServiceIdentifier

from .models import Job
from . import API_NAME, SERVICE_VERSION
from .formatters import JobsFormatOne, JobsFormatMany

__all__ = ['JobsStatus']


class JobsStatus(ServiceIdentifier, JobsFormatOne):
    """Show status of a specific job
    """
    VERBOSITY = Verbosity.BRIEF

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = Job().get_headers(self.VERBOSITY, parsed_args.formatter)
        rec = self.tapis_client.jobs.get(jobId=parsed_args.identifier)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
