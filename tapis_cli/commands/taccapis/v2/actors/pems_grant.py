from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from .mixins import ActorIdentifier
from tapis_cli.commands.taccapis.model import AbacoPermission

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany

__all__ = ['ActorsPemsGrant']


class ActorsPemsGrant(ActorsFormatMany, ActorIdentifier, Username):
    """Grant Permissions on an Actor to a User
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsGrant, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        parser.add_argument('permission',
                            metavar='<permission>',
                            choices=AbacoPermission.NAMES,
                            help='Permission string ({0})'.format('| '.join(
                                AbacoPermission.NAMES)))
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        headers = self.render_headers(AbacoPermission, parsed_args)
        permission = parsed_args.permission
        body = {'user': parsed_args.username, 'level': permission.upper()}
        grant_result = self.tapis_client.actors.updatePermissions(
            actorId=actor_id, body=body)

        records = []
        for key in grant_result:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                username = key
                permission = grant_result[key]
                record.append(username)
                record.append(permission)
            else:
                val = grant_result
                record.append(val)
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
