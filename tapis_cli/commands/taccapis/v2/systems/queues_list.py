from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import SystemQueue
from .formatters import SystemsFormatMany

__all__ = ['SystemsQueuesList']

# TODO - systems queue stats will display the 'load' record for a single queue
# SystemsQueuesStats


class SystemsQueuesList(SystemsFormatMany, ServiceIdentifier):
    """List virtual queues on a System
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsFormatMany, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatMany.preprocess_args(self, parsed_args)
        API_PATH = '{0}/queues'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
        self.update_payload(parsed_args)

        headers = SearchableCommand.render_headers(self, SystemQueue,
                                                   parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
