from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Nonce

__all__ = ['ActorsNoncesCreate']


class ActorsNoncesCreate(ActorsFormatOne, ActorIdentifier):

    HELP_STRING = 'Create a Nonce for the specified Actor'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsNoncesCreate, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser.add_argument('--level',
                            metavar='LEVEL',
                            type=str,
                            required=False,
                            default='EXECUTE',
                            help='Optional Permissions level for this \
                                  Nonce (default: EXECUTE)')
        parser.add_argument(
            '--max-uses',
            metavar='INT',
            type=int,
            required=False,
            default=-1,
            help=
            'Optional Max number of times Nonce can be redeemed (default: -1)',
        )
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        body = {'level': parsed_args.level, 'maxUses': parsed_args.max_uses}
        rec = self.tapis_client.actors.addNonce(actorId=actor_id, body=body)
        headers = self.render_headers(Nonce, parsed_args)
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
