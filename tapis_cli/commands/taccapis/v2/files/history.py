from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import FileHistory
from .formatters import FilesFormatMany

__all__ = ['FilesHistory']


class FilesHistory(FilesFormatMany, AgaveURI):
    """List history for an specific file or directory
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = FilesFormatMany.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatMany.preprocess_args(self, parsed_args)

        headers = SearchableCommand.render_headers(self, FileHistory, parsed_args)
        (system_id, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        results = self.tapis_client.files.getHistory(filePath=file_path,
                                                     systemId=system_id,
                                                     offset=parsed_args.offset,
                                                     limit=parsed_args.limit)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
