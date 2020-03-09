from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.utils import fnmatches

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany

from tapis_cli.utils import fnmatches
from .models import Alias
from .mixins import GlobListFilter

__all__ = ['ActorsAliasesList']


class ActorsAliasesList(ActorsFormatMany, GlobListFilter):

    HELP_STRING = 'List all Actor Aliases'
    LEGACY_COMMMAND_STRING = 'abaco aliases list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE
    FILTERABLE_KEYS = Alias.FILTERABLE_KEYS

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesList, self).get_parser(prog_name)
        parser = GlobListFilter.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)
        results = self.tapis_client.actors.listAliases()
        headers = self.render_headers(Alias, parsed_args)

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
