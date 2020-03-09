from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from tapis_cli.commands.taccapis.model import Permission
from .formatters import FilesPemsFormatMany
from .mixins import FileOptions
from .helpers.pems_list import pems_list

__all__ = ['FilesPemsList']


class FilesPemsList(FilesPemsFormatMany, AgaveURI, FileOptions):

    HELP_STRING = 'List permissions for an specific Files path'
    LEGACY_COMMMAND_STRING = 'files-pems-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = FilesPemsFormatMany.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = FileOptions.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesPemsFormatMany.preprocess_args(self, parsed_args)
        headers = Permission.get_headers(self, self.VERBOSITY,
                                         parsed_args.formatter)
        self.update_payload(parsed_args)
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        results = pems_list(file_path,
                            system_id=storage_system,
                            limit=parsed_args.limit,
                            offset=parsed_args.offset,
                            permissive=False,
                            agave=self.tapis_client)

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
