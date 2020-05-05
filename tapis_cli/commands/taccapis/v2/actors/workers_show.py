from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import (ActorIdentifier, WorkerIdentifier)
from .models import Worker

__all__ = ['ActorsWorkersShow']


class ActorsWorkersShow(ActorsFormatOne, ActorIdentifier, WorkerIdentifier):

    HELP_STRING = 'Show details for a Worker'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersShow, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = WorkerIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        worker_id = WorkerIdentifier().get_identifier(parsed_args)
        results = self.tapis_client.actors.getWorker(actorId=actor_id,
                                                     workerId=worker_id,
                                                     **self.client_extra_args)
        headers = self.render_headers(Worker, parsed_args)
        data = []
        for key in headers:
            try:
                val = results[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
