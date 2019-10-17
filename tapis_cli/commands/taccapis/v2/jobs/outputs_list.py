import os
from tapis_cli.display import Verbosity

from ..files.models import File
from ..files.formatters import FilesFormatMany
from ..files.mixins import FilesOptions
from tapis_cli.clients.services.mixins import JobsUUID, RemoteFilePath
# Note - this is the jobs-outputs specific listdir!
from .helpers.walk import listdir

from . import API_NAME, SERVICE_VERSION


class JobsOutputsList(FilesFormatMany, JobsUUID, FilesOptions, RemoteFilePath):
    """Lists a Jobs output directory
    """
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
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(File, parsed_args)
        recs = listdir(parsed_args.file_path,
                       job_uuid=parsed_args.job_uuid,
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

        return (tuple(headers), tuple(data))
