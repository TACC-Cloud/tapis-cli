from tapis_cli.display import Verbosity
from tapis_cli.utils import fnmatches
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatManyUnlimited
from .models import Execution
from .mixins import GlobListFilter

__all__ = ['ActorsExecsList']


class ActorsExecsList(ActorsFormatManyUnlimited, ActorIdentifier,
                      GlobListFilter):

    HELP_STRING = 'List Executions for a specific Actor'
    LEGACY_COMMMAND_STRING = 'abaco executions'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD
    FILTERABLE_KEYS = Execution.FILTERABLE_KEYS
    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsExecsList, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser = GlobListFilter.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        results = self.tapis_client.actors.listExecutions(
            actorId=actor_id, **self.client_extra_args)
        # custom headers to print all the execution id and status for a
        # given actor id
        execs_result = results.get('executions')    # returns a list
        headers = ["executionId", "status"]

        records = []
        for rec in execs_result:

            include = False
            if parsed_args.list_filter is None:
                include = True
            else:
                for k in self.FILTERABLE_KEYS:
                    if parsed_args.list_filter in rec[k]:
                        include = True
                    elif fnmatches(rec[k], [parsed_args.list_filter]):
                        include = True

            if include:
                record = []
                record.append(rec.get('id'))
                record.append(rec.get('status'))
                if record not in records:
                    records.append(record)

        return (tuple(headers), tuple(records))
