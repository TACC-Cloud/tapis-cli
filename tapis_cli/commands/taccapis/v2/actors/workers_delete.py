from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import (ActorIdentifier, WorkerIdentifier)

__all__ = ['ActorsWorkersDelete']


class ActorsWorkersDelete(ActorsFormatOne, ActorIdentifier, WorkerIdentifier):

    HELP_STRING = 'Delete a Worker'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersDelete, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = WorkerIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        worker_id = WorkerIdentifier().get_identifier(parsed_args)
        headers = ['deleted', 'messages']
        deleted = []
        messages = []

        try:
            self.tapis_client.actors.deleteWorker(actorId=actor_id,
                                                  workerId=worker_id)
            deleted.append(worker_id)
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]
        return (tuple(headers), tuple(data))
