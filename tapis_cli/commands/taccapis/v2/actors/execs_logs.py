import sys
from tapis_cli.display import Verbosity
from .mixins import (ActorIdentifier, ExecutionIdentifier)

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatManyUnlimited
from .models import Execution

__all__ = ['ActorsExecsLogs']


class ActorsExecsLogs(ActorsFormatManyUnlimited, ActorIdentifier,
                      ExecutionIdentifier):

    HELP_STRING = 'Show logs for a specific Execution'
    LEGACY_COMMMAND_STRING = 'abaco logs'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD
    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsExecsLogs, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = ExecutionIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        exec_id = ExecutionIdentifier().get_identifier(parsed_args)
        results = self.tapis_client.actors.getExecutionLogs(
            actorId=actor_id, executionId=exec_id, **self.client_extra_args)
        headers = ['logs']
        logs_result = results.get('logs')
        print("Logs for execution", exec_id, "\n", logs_result)
        sys.exit(0)
