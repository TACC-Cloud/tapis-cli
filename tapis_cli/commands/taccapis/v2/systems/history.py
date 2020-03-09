from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import SystemHistory
from .formatters import SystemsHistoryFormatMany

__all__ = ['SystemsHistory']


class SystemsHistory(SystemsHistoryFormatMany, ServiceIdentifier):

    HELP_STRING = 'Show history for a System'
    LEGACY_COMMMAND_STRING = 'systems-history'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsHistory, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        API_PATH = '{0}/history'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
        self.update_payload(parsed_args)

        headers = self.render_headers(SystemHistory, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
