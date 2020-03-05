import sys
from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatManyUnlimited
from .models import Execution

__all__ = ['ActorsExecsLogs']


class ActorsExecsLogs(ActorsFormatManyUnlimited, ActorIdentifier):
    """Show specific Actor Execution Logs
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsExecsLogs, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser.add_argument('executionId',
                            metavar='executionId',
                            type=str,
                            help='The id of execution')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        execId = parsed_args.executionId
        results = self.tapis_client.actors.getExecutionLogs(actorId=actor_id,
                                                            executionId=execId)
        headers = ['logs']
        logs_result = results.get('logs')
        print("Logs for execution", execId, "\n", logs_result)
        sys.exit(0)
