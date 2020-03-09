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

    HELP_STRING = 'Search for Metadata documents'
    LEGACY_COMMMAND_STRING = 'metadata-list'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(MetadataFormatMany, self).get_parser(prog_name)
        search_group = parser.add_argument_group('Search arguments')
        # Dont use the SearchableCommand method. Instead, build up
        # query manually since the metadata service is the only example of
        # this dialect for querying the backing MongoDB
        for f in Metadata().fields:
            if f.searchable:
                sarg = SearchMongoQuery(argument=f.param_name,
                                        field_type=f.param_type,
                                        mods=f.mod_types,
                                        default_mod=f.default_mod)
                self._cache_sarg(sarg)
                sargp = sarg.get_argparse()
                search_group.add_argument(sargp.argument, **sargp.attributes)

        parser.add_argument('--privileged',
                            dest='privileged',
                            action='store_false',
                            help='Display or act with privilege')
        return parser

    def update_payload(self, parsed_args):
        # Override inherited update_payload to add --privileged
        super(MetadataSearch, self).update_payload(parsed_args)
        self.post_payload['privileged'] = parsed_args.privileged
        return self

    def take_action(self, parsed_args):
        parsed_args = MetadataFormatMany.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)

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
        # print(self.post_payload['q'])

        headers = SearchableCommand.render_headers(self, Metadata, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
