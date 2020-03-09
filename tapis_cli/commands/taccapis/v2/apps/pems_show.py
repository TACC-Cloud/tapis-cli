from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from .mixins import AppIdentifier
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import AppsFormatOne

__all__ = ['AppsPemsShow']


class AppsPemsShow(AppsFormatOne, AppIdentifier, Username):

    HELP_STRING = 'Show Permissions on an App for specific User'
    LEGACY_COMMMAND_STRING = 'apps-pems-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsPemsShow, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)
        # Below is call to the AgavePy method but it is broken due to changes in behavior
        # between Py2 and Py3. It returns an wierdly iterated dict object:
        #
        # {'u': 'username', 's': 'username', 'e': 'username', 'r': 'username', 'n': 'username', 'a': 'username', 'm': 'username'}
        # rather than the expected dict of username & permission object
        #
        # rec = self.tapis_client.apps.listPermissionsForUser(
        #   appId=app_id, username=parsed_args.username)
        #
        # Instead, we use the Command's requests client which returns a
        # very simple response:
        # {"username": "<username>",
        #  "permission": {"write": bool, "read": bool, "exceute": bool, "_links": []}
        #
        API_PATH = '{0}/pems/{1}'.format(app_id, parsed_args.username)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)

        headers = self.render_headers(Permission, parsed_args)
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
            record.extend(Permission.pem_to_row(rec.get('permission', {})))
        else:
            # Verbose JSON display
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)

        return (headers, record)
