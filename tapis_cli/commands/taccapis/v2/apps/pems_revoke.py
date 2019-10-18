from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier, Username
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import AppsFormatMany

__all__ = ['AppsPemsRevoke']


class AppsPemsRevoke(AppsFormatMany, ServiceIdentifier, Username):
    """Revoke Permissions on an App for a User
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsPemsRevoke, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)

        body = {'username': parsed_args.username, 'permission': 'NONE'}
        headers = self.render_headers(Permission, parsed_args)
        revoke_result = self.tapis_client.apps.updateApplicationPermissions(
            appId=parsed_args.identifier, body=body)
        results = self.tapis_client.apps.listPermissions(
            appId=parsed_args.identifier)

        records = []
        for rec in results:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                record.append(rec.get('username'))
                record.extend(Permission.pem_to_row(rec.get('permission', {})))
            else:
                for key in headers:
                    val = self.render_value(rec.get(key, None))
                    record.append(val)
            # Deal with an API-side bug where >1 identical pems are
            # returned for the owning user when no additional pems have been
            # granted on the app
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
