from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Worker

__all__ = ['ActorsWorkersCreate']


class ActorsWorkersCreate(ActorsFormatOne, ActorIdentifier):

    HELP_STRING = 'Add Workers to the specified Actor'
    LEGACY_COMMMAND_STRING = 'abaco workers'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersCreate, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser.add_argument('num',
                            metavar='INT',
                            type=int,
                            help='The number of workers to ensure are running;\
                            Note:Only Admins are authorized to update workers',
                            default=1)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        num = parsed_args.num
        body = {'num': num}
        create_result = self.tapis_client.actors.addWorker(actorId=actor_id,
                                                           body=body)
        headers = self.render_headers(Worker, parsed_args)
        # worker names are in a list
        data = []
        for key in headers:
            try:
                val = create_result[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
