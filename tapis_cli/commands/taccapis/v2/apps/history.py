from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import AppHistory
from .formatters import AppsFormatMany

__all__ = ['AppsHistory']


class AppsHistory(AppsFormatMany, ServiceIdentifier):
    """List history for an specific app
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = AppsFormatMany.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = AppsFormatMany.before_take_action(self, parsed_args)
        api_resource = '{0}/history'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, api_resource)

        headers = SearchableCommand.headers(self, AppHistory, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
