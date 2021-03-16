from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Alias
from .mixins import AliasIdentifier

__all__ = ['ActorsAliasesCreate']


class ActorsAliasesCreate(ActorsFormatOne, ActorIdentifier, AliasIdentifier):

    HELP_STRING = 'Add an Alias for an Actor'
    LEGACY_COMMMAND_STRING = 'abaco aliases create'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesCreate, self).get_parser(prog_name)
        parser = AliasIdentifier().extend_parser(parser)
        parser = ActorIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        alias = AliasIdentifier().get_identifier(parsed_args)
        body = {'actorId': actor_id, 'alias': alias}
        rec = self.tapis_client.actors.addAlias(body=body)
        headers = self.render_headers(Alias, parsed_args)
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
