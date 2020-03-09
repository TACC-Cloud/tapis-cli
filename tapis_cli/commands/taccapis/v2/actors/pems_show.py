from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier
from tapis_cli.clients.services.mixins import Username
from tapis_cli.commands.taccapis.model import AbacoPermission

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsPemsShow']


class ActorsPemsShow(ActorsFormatOne, ActorIdentifier, Username):

    HELP_STRING = 'Show User-specific Permissions for an Actor'
    LEGACY_COMMMAND_STRING = 'abaco permissions'
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsShow, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = Username().extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        user = parsed_args.username
        results = self.tapis_client.actors.getPermissions(actorId=actor_id)
        headers = self.render_headers(AbacoPermission, parsed_args)
        username = []
        permission = []

        if user in results:
            username.append(user)
            permission.append(results[user])
        else:
            username.append('None')
            permission.append('None')
        data = [username[0], permission[0]]

        return (tuple(headers), tuple(data))
