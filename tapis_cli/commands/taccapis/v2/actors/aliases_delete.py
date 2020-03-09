from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import AliasIdentifier

__all__ = ['ActorsAliasesDelete']


class ActorsAliasesDelete(ActorsFormatOne, AliasIdentifier):

    HELP_STRING = 'Delete an Actor Alias'
    LEGACY_COMMMAND_STRING = 'abaco aliases rm'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesDelete, self).get_parser(prog_name)
        parser = AliasIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        alias_id = AliasIdentifier().get_identifier(parsed_args)

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
