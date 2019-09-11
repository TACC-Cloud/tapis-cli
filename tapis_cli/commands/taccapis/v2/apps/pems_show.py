from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import AppPermission
from .formatters import AppsFormatOne

__all__ = ['AppsPemsShow']


class AppsPemsShow(AppsFormatOne, ServiceIdentifier):
    """Show permissions on an app for specific user
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = AppsFormatOne.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser.add_argument('username',
                            type=str,
                            help='username to show permission for')
        return parser

    def take_action(self, parsed_args):
        parsed_args = AppsFormatOne.before_take_action(self, parsed_args)
        headers = AppPermission.get_headers(self, self.VERBOSITY,
                                            parsed_args.formatter)
        #
        # Below is call to the AgavePy method but it is broken due to changes in behavior
        # between Py2 and Py3. It returns an wierdly iterated dict object:
        #
        # {'u': 'username', 's': 'username', 'e': 'username', 'r': 'username', 'n': 'username', 'a': 'username', 'm': 'username'}
        # rather than the expected dict of username & permission object
        #
        # rec = self.tapis_client.apps.listPermissionsForUser(
        #   appId=parsed_args.identifier, username=parsed_args.username)
        #
        # Instead, we use the Command's requests client which returns a
        # very simple response:
        # {"username": "<username>",
        #  "permission": {"write": bool, "read": bool, "exceute": bool, "_links": []}
        #
        API_PATH = '{0}/pems/{1}'.format(parsed_args.identifier,
                                         parsed_args.username)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
        rec = self.requests_client.get_data(params=self.post_payload)

        # TODO - Account for the wierd behavior where querying ANY username
        # will return +rwx even if the username is fictitious. A client-side
        # (partial) would be to list the pems, extract the usernames, and
        # validate presence of <username> among the. Another would be to
        # simply list all pems and extract the matching row by <username>

        record = []
        if self.app_verbose_level > self.VERBOSITY:
            # Table display
            record.append(rec.get('username'))
            record.extend(AppPermission.pem_to_row(rec.get('permission', {})))
        else:
            # Verbose JSON display
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)

        return (headers, record)
