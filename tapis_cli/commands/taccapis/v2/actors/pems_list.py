from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier
from tapis_cli.commands.taccapis.model import AbacoPermission

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany

__all__ = ['ActorsPemsList']


class ActorsPemsList(ActorsFormatMany, ActorIdentifier):
    """Show Permissions on an Actor
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsList, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        headers = self.render_headers(AbacoPermission, parsed_args)
        results = self.tapis_client.actors.getPermissions(actorId=actor_id)

        # TODO - Account for the wierd behavior where querying ANY username
        # will return +rwx even if the username is fictitious. A client-side
        # (partial) would be to list the pems, extract the usernames, and
        # validate presence of <username> among the. Another would be to
        # simply list all pems and extract the matching row by <username>
        # for actors this will return a dictionary with key, values:
        # {"username":"permission"} , so we need to parse this differently

        records = []
        for key in results:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                username = key
                permission = results[key]
                record.append(username)
                record.append(permission)
            else:
                for key in headers:
                    val = self.render_value(results.get(key, None))
                    record.append(val)
            if record not in records:
                records.append(record)

        return(tuple(headers), tuple(records))
