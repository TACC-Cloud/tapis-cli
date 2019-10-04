import os
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .helpers.walk import listdir
from .models import File
from .formatters import FilesFormatMany
from .mixins import FilesOptions

__all__ = ['FilesList']


class FilesList(FilesFormatMany, AgaveURI, FilesOptions):
    """Lists a Files path
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    # TODO - add formatting and sorting options

    def get_parser(self, prog_name):
        parser = FilesFormatMany.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = FilesOptions.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = super().before_take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, File, parsed_args)
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        recs = listdir(file_path,
                       system_id=storage_system,
                       agave=self.tapis_client)
        # recs = self.tapis_client.files.list(systemId=storage_system,
        #                                     filePath=file_path,
        #                                     limit=parsed_args.limit,
        #                                     offset=parsed_args.offset)

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

        return (tuple(headers), tuple(data))
