from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParamEqualsOnly as SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatMany

__all__ = ['ProfilesSearch']


class ProfilesSearch(ProfilesFormatMany):

    HELP_STRING = 'Search by attribute for a Profile'
    LEGACY_COMMMAND_STRING = 'profiles-search'

    VERBOSITY = Verbosity.LISTING

    def get_parser(self, prog_name):
        parser = super(ProfilesSearch, self).get_parser(prog_name)
        # THe search params are created this way instead of with
        # SearchableCommand.extend_parser because the parameterization
        # for profiles is unlike any of the other Tapis services
        #
        # Define a mutually exclusive group for profiles search terms so
        # that only one term can be specified
        search_args = parser.add_mutually_exclusive_group(required=False)
        for f in Profile().fields:
            if f.searchable:
                sarg = SearchWebParam(argument=f.param_name,
                                      field_type=f.param_type,
                                      mods=f.mod_types,
                                      default_mod=f.default_mod)
                self._cache_sarg(sarg)
                sargp = sarg.get_argparse()
                search_args.add_argument(sargp.argument, **sargp.attributes)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        # Set up default search query payload (at minimum: limits, offset)
        # Map properties set in parsed_args to a query payload for search
        filters = list()
        for sarg_name, sarg in self.search_args.items():
            # raise SystemError(sarg.destination)
            parsed_args_val = getattr(parsed_args, sarg.destination, None)
            if parsed_args_val:
                filt = sarg.get_param(parsed_args_val)
                filters.append(filt)

        if len(filters) > 1:
            raise ValueError(
                'Multiple search terms are not supported for this command')

        for f in filters:
            k = list(f.keys())[0]
            v = f[k]
            self.post_payload[k] = v

        self.update_payload(parsed_args)

        headers = self.render_headers(Profile, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
