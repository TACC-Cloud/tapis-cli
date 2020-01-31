from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Execution

__all__ = ['ActorsExecsShow']


class ActorsExecsShow(ActorsFormatOne, ActorIdentifier):
    """Show Executions about a specific Actor Execution
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsExecsShow, self).get_parser(prog_name)
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
        results = self.tapis_client.actors.getExecution(
            actorId=actor_id, executionId=execId)
        headers = self.render_headers(Execution, parsed_args)
        data = []
        for key in headers:
            try:
                val = results[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
