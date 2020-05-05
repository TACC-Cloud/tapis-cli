from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.utils import fnmatches

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatManyUnlimited
from .mixins import ActorIdentifier
from .models import Worker
from .mixins import GlobListFilter

__all__ = ['ActorsWorkersList']


class ActorsWorkersList(ActorsFormatManyUnlimited, ActorIdentifier,
                        GlobListFilter):

    HELP_STRING = 'List Workers for an Actor'
    LEGACY_COMMMAND_STRING = 'abaco workers'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE
    FILTERABLE_KEYS = Worker.FILTERABLE_KEYS

    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersList, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = GlobListFilter().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        glob_filt = parsed_args.list_filter
        results = self.tapis_client.actors.listWorkers(
            actorId=actor_id, **self.client_extra_args)
        headers = ["workerId", "status"]
        records = []
        for rec in results:

            include = False
            if glob_filt is None:
                include = True
            else:
                for k in self.FILTERABLE_KEYS:
                    if glob_filt in rec[k]:
                        include = True
                    elif fnmatches(rec[k], [glob_filt]):
                        include = True

            if include:
                record = []
                record.append(rec.get('id'))
                record.append(rec.get('status'))
                if record not in records:
                    records.append(record)

        return (tuple(headers), tuple(records))
