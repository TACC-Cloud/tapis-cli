from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import ActorIdentifier
from .models import Worker

__all__ = ['ActorsWorkersShow']


class ActorsWorkersShow(ActorsFormatOne, ActorIdentifier):

    DESCRIPTION = 'Show details of a specific Worker'
    LEGACY_COMMMAND = None
    
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersShow, self).get_parser(prog_name)
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
        results = self.tapis_client.actors.getWorker(actorId=actor_id,
                                                     workerId=worker_id)
        headers = self.render_headers(Worker, parsed_args)
        data = []
        for key in headers:
            try:
                val = results[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
