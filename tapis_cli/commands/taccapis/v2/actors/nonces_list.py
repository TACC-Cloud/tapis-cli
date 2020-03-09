from tapis_cli.display import Verbosity
from tapis_cli.utils import fnmatches

from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatManyUnlimited
from .models import Nonce
from .mixins import GlobListFilter

__all__ = ['ActorsNoncesList']


class ActorsNoncesList(ActorsFormatManyUnlimited, ActorIdentifier,
                       GlobListFilter):

    HELP_STRING = 'List Nonces for the specified Actor'
    LEGACY_COMMMAND_STRING = None

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD
    FILTERABLE_KEYS = Nonce.FILTERABLE_KEYS

    def get_parser(self, prog_name):
        parser = super(ActorsNoncesList, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = GlobListFilter.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        results = self.tapis_client.actors.listNonces(actorId=actor_id)

        headers = self.render_headers(Nonce, parsed_args)
        records = []
        for rec in results:

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
                for key in headers:
                    val = self.render_value(rec.get(key, None))
                    record.append(val)
                records.append(record)

        return (tuple(headers), tuple(records))
