import json
import urllib.parse
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchMongoQuery
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne, MetadataFormatMany

__all__ = ['MetadataSearch']

# Figure out how to implement -P (search by associationIds) as it errors with
# "Unable to contact api server at https://<server>/meta/v2" when called in
# the current Bash CLI. Must not be critical...


class MetadataSearch(MetadataFormatMany, SearchableCommand):
    """Search the Metadata catalog
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(MetadataFormatMany, self).get_parser(prog_name)
        parser.add_argument('--privileged',
                            dest='privileged',
                            action='store_false',
                            help='Display or act with privilege')

        for f in Metadata().fields:
            if f.searchable:
                sarg = SearchMongoQuery(argument=f.param_name,
                                        field_type=f.param_type,
                                        mods=f.mod_types,
                                        default_mod=f.default_mod)
                self.cache_sarg(sarg)
                sargp = sarg.get_argparse()
                parser.add_argument(sargp.argument, **sargp.attributes)
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.post_payload['privileged'] = parsed_args.privileged

        # Map properties set in parsed_args to a payload for the 'q' param
        # Note that this is different from how we usually construct the
        # parameters payload!
        filters = list()
        mongoql_els = dict()
        for sarg_name, sarg in self.search_args.items():
            # raise SystemError(sarg.destination)
            parsed_args_val = getattr(parsed_args, sarg.destination, None)
            if parsed_args_val:
                filt = sarg.get_param(parsed_args_val)
                filters.append(filt)
        for f in filters:
            k = list(f.keys())[0]
            v = f[k]
            mongoql_els[k] = v
        self.post_payload['q'] = json.dumps(mongoql_els)

        self.take_action_defaults(parsed_args)

        headers = Metadata().get_headers(self.VERBOSITY, parsed_args.formatter)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
