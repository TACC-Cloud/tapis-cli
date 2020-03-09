from tapis_cli.display import Verbosity
from .mixins import AppIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import AppHistory
from .formatters import AppsFormatMany

__all__ = ['AppsHistory']


class AppsHistory(AppsFormatMany, AppIdentifier):

    HELP_STRING = 'Show history for an App'
    LEGACY_COMMMAND_STRING = 'apps-history'

    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsHistory, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)

        api_resource = '{0}/history'.format(app_id)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, api_resource)

        headers = self.render_headers(AppHistory, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)

        return (tuple(headers), tuple(records))
