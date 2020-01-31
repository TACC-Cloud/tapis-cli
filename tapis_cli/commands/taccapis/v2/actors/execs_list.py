from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany
from .models import Execution

__all__ = ['ActorsExecsList']


class ActorsExecsList(ActorsFormatMany, ActorIdentifier):
    """List Executions for a specific Actor
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsExecsList, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        results = self.tapis_client.actors.listExecutions(
            actorId=actor_id)
        # custom headers to print all the execution id and status for a
        # given actor id
        execs_result = results.get('executions') # returns a list
        headers = ["executionId", "status"]

        records = []
        for rec in execs_result:
            record = []
            record.append(rec.get('id'))
            record.append(rec.get('status'))
            if record not in records:
                records.append(record)
        return (tuple(headers), tuple(records))
