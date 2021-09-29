from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import (ActorIdentifier, NonceIdentifier)

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Nonce

__all__ = ['ActorsNoncesShow']


class ActorsNoncesShow(ActorsFormatOne, ActorIdentifier, NonceIdentifier):

    HELP_STRING = 'Show details for a Nonce attached to an Actor (or Alias)'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsNoncesShow, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = NonceIdentifier().extend_parser(parser)
        parser.add_argument(
            '-A',
            dest='is_alias',
            action='store_true',
            help='Identifier is an ALIAS rather than an ACTOR_ID')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        nonce_id = NonceIdentifier().get_identifier(parsed_args)
        # Use the requests_client because AgavePy is not configured
        # with the alias-specific nonces endpoint
        if parsed_args.is_alias:
            api_path = 'aliases/' + actor_id + '/nonces/' + nonce_id
            self.requests_client.setup(API_NAME, SERVICE_VERSION, api_path)
            rec = self.requests_client.get()
        else:
            rec = self.tapis_client.actors.listNonces(actorId=actor_id)

        headers = self.render_headers(Nonce, parsed_args)
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
