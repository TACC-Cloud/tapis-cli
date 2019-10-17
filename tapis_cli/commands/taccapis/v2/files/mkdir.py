import os
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier, AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.utils import abspath

from . import API_NAME, SERVICE_VERSION
from .models import FileStaging
from .formatters import FilesFormatOne
from .mixins import FileOptions
from .helpers.manage import makedirs

__all__ = ['FilesMakeDir']


class FilesMakeDir(FilesFormatOne, AgaveURI, FileOptions):
    """Create a Files directory
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser.add_argument(
            'dir_name',
            metavar='<dir_name>',
            help='Name of the new directory (relative to <agave_uri>)')
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.render_headers(self, FileStaging, parsed_args)
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        dir_name = parsed_args.dir_name
        if dir_name is None:
            dir_name = ''
        rec = makedirs(dir_name,
                       system_id=storage_system,
                       destination=file_path,
                       exist_ok=True,
                       permissive=False,
                       agave=self.tapis_client)
        # rec = self.tapis_client.files.list(systemId=storage_system,
        #                                    filePath=file_path,
        #                                    limit=1,
        #                                    offset=0)
        # if isinstance(rec, list):
        #     rec = rec[0]
        # else:
        #     raise ValueError('No files listing was returned')

        # Fixes issue where the name of the listed file/directory is not
        # returned by the files service
        if rec['name'] == '.':
            rec['name'] = os.path.basename(rec['path'])
        # Coerce path to absolute path
        rec['path'] = abspath(rec['path'], '/')

        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
