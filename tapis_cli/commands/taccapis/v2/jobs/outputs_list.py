import os
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import RemoteFilePath

from ..files.models import File
from .formatters import JobsFormatMany
from ..files.mixins import FilesOptions
# Note - this is the jobs-outputs specific listdir!
from .helpers.walk import listdir
from .mixins import JobsUUID
from . import API_NAME, SERVICE_VERSION


class JobsOutputsList(JobsFormatMany, JobsUUID, FilesOptions, RemoteFilePath):

    HELP_STRING = 'Lists output directory for a Jobs'
    LEGACY_COMMMAND_STRING = 'jobs-output-list'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsOutputsList, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        parser = RemoteFilePath.extend_parser(self, parser)
        parser = FilesOptions.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(File, parsed_args)
        recs = listdir(parsed_args.file_path,
                       job_uuid=identifier,
                       dotfiles=parsed_args.dotfiles,
                       agave=self.tapis_client)

        if not isinstance(recs, list):
            raise ValueError('No listing was returned')

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
