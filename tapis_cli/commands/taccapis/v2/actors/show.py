from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import ActorIdentifier
from .models import Actor

__all__ = ['ActorsShow']


class ActorsShow(ActorsFormatOne, ActorIdentifier):

    HELP_STRING = 'Show details for an Actor'
    LEGACY_COMMMAND_STRING = 'abaco list'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsShow, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = self.render_headers(Actor, parsed_args)
        rec = self.tapis_client.actors.get(actorId=actor_id,
                                           **self.client_extra_args)

        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
