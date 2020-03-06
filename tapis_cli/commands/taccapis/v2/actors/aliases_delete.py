from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsAliasesDelete']


class ActorsAliasesDelete(ActorsFormatOne):

    DESCRIPTION = 'Delete an Alias'
    LEGACY_COMMMAND = 'abaco aliases rm'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesDelete, self).get_parser(prog_name)
        parser.add_argument('alias',
                            metavar='<ALIAS>',
                            help='The id of the alias to delete')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        alias_id = parsed_args.alias

        headers = ['deleted', 'messages']
        deleted = []
        messages = []

        try:
            self.tapis_client.actors.deleteAlias(alias=alias_id)
            deleted.append(alias_id)
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]

        return (tuple(headers), tuple(data))
