from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import AppPermission
from .formatters import AppsFormatMany

__all__ = ['AppsPemsList']


class AppsPemsList(AppsFormatMany, ServiceIdentifier):
    """List permissions for an specific app
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = AppsFormatMany.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = AppsFormatMany.before_take_action(self, parsed_args)
        headers = AppPermission.get_headers(self, self.VERBOSITY,
                                            parsed_args.formatter)
        self.take_action_defaults(parsed_args)

        results = self.tapis_client.apps.listPermissions(
            appId=parsed_args.identifier)

        records = []
        for rec in results:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                record.append(rec.get('username'))
                record.extend(
                    AppPermission.pem_to_row(rec.get('permission', {})))
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
