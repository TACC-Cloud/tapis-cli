import os
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import AgaveURI

from . import API_NAME, SERVICE_VERSION
from .helpers.walk import listdir
from .models import File
from .formatters import FilesFormatMany
from .mixins import FilesOptions

__all__ = ['FilesList']


class FilesList(FilesFormatMany, AgaveURI, FilesOptions):

    HELP_STRING = 'List contents of a Files path'
    LEGACY_COMMMAND_STRING = 'files-list'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    # TODO - add formatting and sorting options

    def get_parser(self, prog_name):
        parser = super(FilesList, self).get_parser(prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = FilesOptions.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        (storage_system, file_path) = self.parse_url(parsed_args.agave_uri)
        headers = self.render_headers(File, parsed_args)
        recs = listdir(file_path,
                       dotfiles=parsed_args.dotfiles,
                       system_id=storage_system,
                       agave=self.tapis_client)

        if not isinstance(recs, list):
            raise ValueError('No files listing was returned')

        data = []

        # Fixes issue where the name of the listed file/directory is not
        # returned by the files service
        for rec in recs:
            row = []
            if rec['name'] == '.':
                rec['name'] = os.path.basename(rec['path'])

            for key in headers:
                try:
                    val = rec[key]
                except KeyError:
                    val = None
                row.append(val)
            data.append(row)

        # Sort must happen before humanize since it will affect sort order
        if parsed_args.ls_sort_time:
            sort_header = 'lastModified'
        elif parsed_args.ls_sort_size:
            sort_header = 'length'
        else:
            sort_header = 'name'
        data = self.sort_table(data,
                               headers,
                               header=sort_header,
                               reverse=parsed_args.ls_sort_reverse)

        # In-place field render (mostly for fixing datetime at this point)
        fdata = []
        for row in data:
            row_data = [self.render_value(v) for v in row]
            fdata.append(row_data)

        return (tuple(headers), tuple(fdata))
