from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import JobsFormatMany
from .mixins import JobsUUID

__all__ = ['JobsPemsList']


class JobsPemsList(JobsFormatMany, JobsUUID):

    HELP_STRING = 'List Permissions for a Job'
    LEGACY_COMMMAND_STRING = 'jobs-pems-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(JobsPemsList, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = JobsUUID.get_identifier(self, parsed_args)
        self.update_payload(parsed_args)

        headers = self.render_headers(Permission, parsed_args)
        results = self.tapis_client.jobs.listPermissions(jobId=identifier)

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
