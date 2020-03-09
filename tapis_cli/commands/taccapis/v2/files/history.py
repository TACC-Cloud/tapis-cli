from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import AgaveURI

from . import API_NAME, SERVICE_VERSION
from .models import FileHistory
from .formatters import FilesFormatMany

__all__ = ['FilesHistory']


class FilesHistory(FilesFormatMany, AgaveURI):

    HELP_STRING = 'List history for a Files'
    LEGACY_COMMMAND_STRING = 'files-history'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(FilesHistory, self).get_parser(prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)

        (system_id, file_path) = self.parse_url(parsed_args.agave_uri)
        headers = self.render_headers(FileHistory, parsed_args)
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
