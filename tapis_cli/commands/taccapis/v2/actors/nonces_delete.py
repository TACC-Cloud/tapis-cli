from tapis_cli.display import Verbosity
from .mixins import (ActorIdentifier, NonceIdentifier)

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsNoncesDelete']


class ActorsNoncesDelete(ActorsFormatOne, ActorIdentifier, NonceIdentifier):

    HELP_STRING = 'Delete a Nonce from an Actor (or Alias)'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsNoncesDelete, self).get_parser(prog_name)
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

        headers = ['deleted', 'messages']
        deleted = []
        messages = []

        try:
            # Use the requests_client because AgavePy is not configured
            # with the alias-specific nonces endpoint
            if parsed_args.is_alias:
                api_path = 'aliases/' + actor_id + '/nonces/' + nonce_id
                self.requests_client.setup(API_NAME, SERVICE_VERSION, api_path)
                rec = self.requests_client.delete()
            else:
                rec = self.tapis_client.actors.deleteNonce(actorId=actor_id,
                                                           nonceId=nonce_id)
            deleted.append(nonce_id)
        except Exception as err:
            messages.append(str(err))

        # # try:
        # #     self.tapis_client.actors.deleteNonce(actorId=actor_id,
        # #                                          nonceId=nonce_id)
        # #     deleted.append(nonce_id)
        # # except Exception as err:
        # #     messages.append(str(err))
        data = [deleted, messages]

        return (tuple(headers), tuple(data))
