from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import SystemHistory
from .formatters import SystemsHistoryFormatMany

__all__ = ['SystemsHistory']


class SystemsHistory(SystemsHistoryFormatMany, ServiceIdentifier):
    """List history of a system
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsHistoryFormatMany, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsHistoryFormatMany.before_take_action(
            self, parsed_args)
        API_PATH = '{0}/history'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, SystemHistory, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
