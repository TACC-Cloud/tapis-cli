from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne, AppsFormatMany

__all__ = ['AppsSearch']


class AppsSearch(AppsFormatMany, SearchableCommand):
    """Search the Apps catalog
    """
    VERBOSITY = Verbosity.LISTING

    def get_parser(self, prog_name):
        parser = super(AppsFormatMany, self).get_parser(prog_name)
        for f in App().fields:
            if f.searchable:
                sarg = SearchWebParam(argument=f.param_name,
                                      field_type=f.param_type,
                                      mods=f.mod_types,
                                      default_mod=f.default_mod)
                self.cache_sarg(sarg)
                sargp = sarg.get_argparse()
                parser.add_argument(sargp.argument, **sargp.attributes)
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        # Set up default search query payload (at minimum: limits, offset)
        self.take_action_defaults(parsed_args)

        # Map properties set in parsed_args to a query payload for search
        filters = list()
        for sarg_name, sarg in self.search_args.items():
            # raise SystemError(sarg.destination)
            parsed_args_val = getattr(parsed_args, sarg.destination, None)
            if parsed_args_val:
                filt = sarg.get_param(parsed_args_val)
                filters.append(filt)

        for f in filters:
            k = list(f.keys())[0]
            v = f[k]
            self.post_payload[k] = v

        results = self.requests_client.get_data(params=self.post_payload)
        headers = App().get_headers(self.VERBOSITY, parsed_args.formatter)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
