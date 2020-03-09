from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import (ActorIdentifier, NonceIdentifier)

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Nonce

__all__ = ['ActorsNoncesShow']


class ActorsNoncesShow(ActorsFormatOne, ActorIdentifier, NonceIdentifier):

    HELP_STRING = 'Show details for a Nonce'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsNoncesShow, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = NonceIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        nonce_id = NonceIdentifier().get_identifier(parsed_args)
        rec = self.tapis_client.actors.getNonce(actorId=actor_id,
                                                nonceId=nonce_id)
        headers = self.render_headers(Nonce, parsed_args)
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
