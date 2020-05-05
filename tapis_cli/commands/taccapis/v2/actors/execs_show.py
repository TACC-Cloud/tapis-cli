from tapis_cli.display import Verbosity
from .mixins import (ActorIdentifier, ExecutionIdentifier)

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Execution

__all__ = ['ActorsExecsShow']


class ActorsExecsShow(ActorsFormatOne, ActorIdentifier, ExecutionIdentifier):

    HELP_STRING = 'Show details of a specific Execution'
    LEGACY_COMMMAND_STRING = 'abaco executions'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsExecsShow, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = ExecutionIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        exec_id = ExecutionIdentifier().get_identifier(parsed_args)
        results = self.tapis_client.actors.getExecution(
            actorId=actor_id, executionId=exec_id, **self.client_extra_args)
        headers = self.render_headers(Execution, parsed_args)
        data = []
        for key in headers:
            try:
                val = results[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
