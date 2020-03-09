from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from .mixins import ActorIdentifier
from tapis_cli.commands.taccapis.model import AbacoPermission

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatManyUnlimited

__all__ = ['ActorsPemsGrant']


class ActorsPemsGrant(ActorsFormatManyUnlimited, ActorIdentifier, Username):

    HELP_STRING = 'Grant Permissions on the specified Actor'
    LEGACY_COMMMAND_STRING = 'abaco permissions'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsGrant, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = Username().extend_parser(parser)
        parser.add_argument('permission',
                            metavar='PERMISSION',
                            choices=AbacoPermission.NAMES,
                            help='Permission name ({0})'.format('| '.join(
                                AbacoPermission.NAMES)))
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        user_id = parsed_args.username
        headers = self.render_headers(AbacoPermission, parsed_args)
        permission = parsed_args.permission
        body = {'user': user_id, 'level': permission.upper()}
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
