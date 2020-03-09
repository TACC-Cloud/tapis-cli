from tapis_cli.display import Verbosity
from tapis_cli.utils import fnmatches

from . import API_NAME, SERVICE_VERSION
from .mixins import GlobListFilter
from .models import Actor
from .formatters import ActorsFormatManyUnlimited

__all__ = ['ActorsList']


class ActorsList(ActorsFormatManyUnlimited, GlobListFilter):

    HELP_STRING = 'List available Actors'
    LEGACY_COMMMAND_STRING = 'abaco list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING_VERBOSE
    FILTERABLE_KEYS = Actor.FILTERABLE_KEYS

    def get_parser(self, prog_name):
        parser = super(ActorsList, self).get_parser(prog_name)
        parser = GlobListFilter.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(Actor, parsed_args)
        # THIS IS THE API COMMAND
        results = self.tapis_client.actors.list()

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
