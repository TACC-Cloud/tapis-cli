from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsAliasesShow']


class ActorsAliasesShow(ActorsFormatOne):
    """Show details for an Actor Alias
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesShow, self).get_parser(prog_name)
        parser.add_argument('alias',
                            metavar='<ALIAS>',
                            help='The id of the alias')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        alias = parsed_args.alias
        rec = self.tapis_client.actors.getAlias(alias=alias)
        headers = ["actorId", "alias", "owner"]
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
