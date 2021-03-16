from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Alias
from .mixins import AliasIdentifier


class NewActorIdentifier(ActorIdentifier):
    dest = 'new_actor_id'


class ActorsAliasesUpdate(ActorsFormatOne, NewActorIdentifier,
                          AliasIdentifier):

    HELP_STRING = 'Update an Alias to resolve to a different Actor'
    LEGACY_COMMMAND_STRING = ''

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesUpdate, self).get_parser(prog_name)
        parser = AliasIdentifier().extend_parser(parser)
        parser = NewActorIdentifier().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = NewActorIdentifier().get_identifier(parsed_args)
        alias = AliasIdentifier().get_identifier(parsed_args)
        body = {'actorId': actor_id, 'alias': alias}
        # Delete original alias
        self.tapis_client.actors.deleteAlias(alias=alias)
        # Create new alias
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
