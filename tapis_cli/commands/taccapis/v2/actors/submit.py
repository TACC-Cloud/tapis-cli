from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Message

__all__ = ['ActorsSubmit']


class ActorsSubmit(ActorsFormatOne, ActorIdentifier):

    HELP_STRING = 'Send an asynchronous message to an Actor'
    LEGACY_COMMMAND_STRING = 'abaco run'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsSubmit, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser.add_argument('message',
                            metavar='STRING',
                            type=str,
                            help='The message to send to the Actor')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        body = {'message': parsed_args.message}
        rec = self.tapis_client.actors.sendMessage(actorId=actor_id, body=body)
        headers = self.render_headers(Message, parsed_args)
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
