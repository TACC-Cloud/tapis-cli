from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import AgaveURI, Username
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import FilesFormatOne

__all__ = ['FilesPemsShow']


class FilesPemsShow(FilesFormatOne, AgaveURI, Username):
    """Show permissions on a file path for specific user
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatOne.before_take_action(self, parsed_args)
        headers = Permission.get_headers(self, self.VERBOSITY,
                                         parsed_args.formatter)
        self.take_action_defaults(parsed_args)

        # We use the Command's requests client since file permissions lookup
        # by user are not supported via the documented API spec.
        #
        # Reponse: {"username": "<username>",
        #           "permission": {"write": bool, "read": bool,
        #            "exceute": bool, "_links": []}
        #
        # <api_server>/files/v2/pems/system/data-sd2e-community/path
        #
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        API_PATH = 'pems/system/{0}{1}'.format(storage_system, file_path)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
        post_payload = {'username.eq': parsed_args.username}
        rec = self.requests_client.get_data(params=post_payload)[0]

        # TODO - Account for the wierd behavior where querying ANY username
        # will return -r-w-x even if the username is fictitious. A client-side
        # (partial) fix would be to list the pems, extract the usernames, and
        # validate presence of <username> among the. Another would be to
        # simply list all pems and extract the matching row by <username>

        record = []
        if self.app_verbose_level > self.VERBOSITY:
            # Table display
            record.append(rec.get('username'))
            record.extend(Permission.pem_to_row(rec.get('permission', {})))
        else:
            # Verbose JSON display
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)

        return (headers, record)
