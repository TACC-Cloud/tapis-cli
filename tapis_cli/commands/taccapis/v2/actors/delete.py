from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import ActorIdentifier
from .models import Actor

__all__ = ['ActorsDelete']


class ActorsDelete(ActorsFormatOne, ActorIdentifier):

    HELP_STRING = 'Delete an Actor'
    LEGACY_COMMMAND_STRING = 'abaco rm'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsDelete, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        #self.requests_client.setup(API_NAME, SERVICE_VERSION)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)

        headers = ['deleted', 'messages']
        deleted = []
        messages = []

        try:
            self.tapis_client.actors.delete(actorId=actor_id)
            deleted.append(actor_id)
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]
        return (tuple(headers), tuple(data))
