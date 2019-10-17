from tapis_cli.search import SearchWebParam
from tapis_cli.display import Verbosity

__all__ = ['SearchableCommand']


class SearchableCommand(object):
    """Manages population of the search arguments option group
    """
    search_args = dict()

    def _cache_sarg(self, search_arg):
        """Caches a search argument"""
        try:
            if search_arg.destination not in list(self.search_args.keys()):
                self.search_args[search_arg.destination] = search_arg
        except Exception:
            raise

    def extend_parser(self, parser, class_name):
        """Adds a named argument to parser for each searchable argument

        Help for each argument is displayed in the special argument group
        """
        search_group = parser.add_argument_group('Search arguments')
        for f in class_name().fields:
            if f.searchable:
                sarg = SearchWebParam(argument=f.param_name,
                                      field_type=f.param_type,
                                      mods=f.mod_types,
                                      choices=f.choices,
                                      default_mod=f.default_mod)
                try:
                    self._cache_sarg(sarg)
                except Exception:
                    pass
                sargp = sarg.get_argparse()
                search_group.add_argument(sargp.argument, **sargp.attributes)
        return parser

    def render_headers(self, tapis_entity_class, parsed_args):
        """Returns headers from a TapisModel based on current verbosity level
        """
        verbose = getattr(self, 'VERBOSITY', Verbosity.LISTING)
        return tapis_entity_class().get_headers(verbose, parsed_args.formatter)
