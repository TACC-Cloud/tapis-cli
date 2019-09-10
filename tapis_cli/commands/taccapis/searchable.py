from tapis_cli.search import SearchWebParam
from tapis_cli.display import Verbosity

__all__ = ['SearchableCommand']


class SearchableCommand(object):
    search_args = dict()

    def cache_sarg(self, search_arg):
        # raise ValueError(search_arg)
        try:
            if search_arg.destination not in list(self.search_args.keys()):
                self.search_args[search_arg.destination] = search_arg
        except Exception:
            raise

    def extend_parser(self, parser, class_name):
        for f in class_name().fields:
            if f.searchable:
                sarg = SearchWebParam(argument=f.param_name,
                                      field_type=f.param_type,
                                      mods=f.mod_types,
                                      default_mod=f.default_mod)
                self.cache_sarg(sarg)
                sargp = sarg.get_argparse()
                parser.add_argument(sargp.argument, **sargp.attributes)
        return parser

    def headers(self, class_def, parsed_args):
        verbose = getattr(self, 'VERBOSITY', Verbosity.LISTING)
        return class_def().get_headers(verbose, parsed_args.formatter)
