from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import AppHistory
from .formatters import AppsFormatMany

__all__ = ['AppsHistory']


class AppsHistory(AppsFormatMany):
    """List history for a specific app
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsHistory, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        api_resource = '{0}/history'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, api_resource)
        # raise AppError(self.requests_client.build_url())
        self.take_action_defaults(parsed_args)

        headers = AppHistory().get_headers(verbosity_level=self.VERBOSITY)
        results = self.requests_client.get_data(params=self.post_payload)
        # results = self.tapis_client.systems.getHistory(
        #     systemId=parsed_args.identifier)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
