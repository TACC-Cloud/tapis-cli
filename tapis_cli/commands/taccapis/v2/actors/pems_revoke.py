from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from .mixins import ActorIdentifier
from tapis_cli.commands.taccapis.model import AbacoPermission

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany

__all__ = ['ActorsPemsRevoke']


class ActorsPemsRevoke(ActorsFormatMany, ActorIdentifier, Username):
    """Revoke Permissions on an Actor for a User
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsRevoke, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        body = {'user': parsed_args.username, 'level': 'NONE'}
        headers = self.render_headers(AbacoPermission, parsed_args)
        revoke_result = self.tapis_client.actors.updatePermissions(
            actorId=actor_id, body=body)

        records = []
        for key in revoke_result:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                username = key
                permission = revoke_result[key]
                record.append(username)
                record.append(permission)
            else:
                val = revoke_result
                record.append(val)
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
