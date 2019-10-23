from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import JobsUUID

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatOne

__all__ = ['JobsShow']


class JobsShow(JobsFormatOne, JobsUUID):
    """Show a specific Job
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(JobsShow, self).get_parser(prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        parser.add_argument('-T',
                            '--template',
                            dest='job_template',
                            action='store_true',
                            help='Job template from verbose')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.validate_identifier(parsed_args.identifier)
        self.update_payload(parsed_args)

        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        rec = self.tapis_client.jobs.get(jobId=parsed_args.identifier)

        if not parsed_args.job_template:
            headers = self.render_headers(Job, parsed_args)
        else:
            if self.formatter_default != 'json':
                raise ValueError(
                    'JSON output must be specified with --format json or -v option'
                )
            else:
                headers = Job.TEMPLATE_KEYS
                rec = Job.transform_response(rec)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
