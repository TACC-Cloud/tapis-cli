from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier
from tapis_cli.clients.services.mixins import Username
from tapis_cli.commands.taccapis.model import AbacoPermission

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsPemsShow']


class ActorsPemsShow(ActorsFormatOne, ActorIdentifier, Username):
    """Show Permissions on an Actor for a user
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsShow, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
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
        data = [username, permission]

        return (tuple(headers), tuple(data))
