import os
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier, AgaveURI
from tapis_cli.utils import abspath

from . import API_NAME, SERVICE_VERSION
from .models import FileStaging
from .formatters import FilesFormatOne
from .mixins import FileOptions
from .helpers.manage import makedirs

__all__ = ['FilesMakeDir']


class FilesMakeDir(FilesFormatOne, AgaveURI, FileOptions):

    HELP_STRING = 'Create a directory on a System'
    LEGACY_COMMMAND_STRING = 'files-mkdir'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(FilesMakeDir, self).get_parser(prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser.add_argument(
            'dir_name',
            metavar='DIRECTORY',
            help='Name of the new directory (relative to <agave_uri>)')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        dir_name = parsed_args.dir_name
        if dir_name is None:
            dir_name = ''

        headers = self.render_headers(FileStaging, parsed_args)
        rec = makedirs(dir_name,
                       system_id=storage_system,
                       destination=file_path,
                       exist_ok=True,
                       permissive=False,
                       agave=self.tapis_client)

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
