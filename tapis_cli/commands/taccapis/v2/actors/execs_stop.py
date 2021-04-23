from tapis_cli.display import Verbosity
from tapis_cli.utils import fnmatches
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Execution
from .mixins import GlobListFilter

__all__ = ['ActorsExecsStop']


class ActorsExecsStop(ActorsFormatOne, ActorIdentifier):

    HELP_STRING = 'Delete queued messages from the Actor mailbox, preventing their execution. Running executions will continue.'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD
    FILTERABLE_KEYS = Execution.FILTERABLE_KEYS
    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsExecsStop, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        orig_messages_count = self.tapis_client.actors.getMessages(
            actorId=actor_id, **self.client_extra_args).get('messages', -1)
        try:
            results = self.tapis_client.actors.deleteMessages(
                actorId=actor_id, **self.client_extra_args)
        except KeyError:
            # The KeyError is raised because the OpenAPI def for
            # deleteMessages is missing the corresponding
            # response class. It is OK to swallow this error.
            # TODO - remove this once ActorMessagesDeleteResponse is added to https://github.com/TACC/agavepy/blob/bd948d6da9be7e84b5330aa4d5fe1e07d82ad34c/agavepy/resources/api_actors.json.j2
            pass
        except Exception:
            raise
        new_messages_count = self.tapis_client.actors.getMessages(
            actorId=actor_id, **self.client_extra_args).get('messages', -1)
        # custom headers to print all the execution id and status for a
        # given actor id
        headers = [
            "original_message_queue_length", "current_message_queue_length"
        ]
        records = [orig_messages_count, new_messages_count]

        return (tuple(headers), tuple(records))
