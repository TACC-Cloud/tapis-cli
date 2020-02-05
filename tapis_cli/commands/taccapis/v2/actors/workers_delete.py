from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import ActorIdentifier

__all__ = ['ActorsWorkersDelete']


class ActorsWorkersDelete(ActorsFormatOne, ActorIdentifier):
    """Delete a Worker of an Actor
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersDelete, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser.add_argument('workerId',
                            metavar='workerId',
                            type=str,
                            help='The id of worker')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        worker_id = parsed_args.workerId
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
