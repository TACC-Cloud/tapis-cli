__all__ = ['SearchableCommand']


class SearchableCommand:
    search_args = dict()

    def cache_sarg(self, search_arg):
        # raise ValueError(search_arg)
        try:
            if search_arg.destination not in list(self.search_args.keys()):
                self.search_args[search_arg.destination] = search_arg
        except Exception:
            raise
