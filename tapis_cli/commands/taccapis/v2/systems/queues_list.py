from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import SystemQueue
from .formatters import SystemsFormatOne, SystemsFormatMany

__all__ = ['SystemsQueuesList']

# TODO - systems queue stats will display the 'load' record for a single queue
# SystemsQueuesStats


class SystemsQueuesList(ServiceIdentifier, SystemsFormatMany):
    """List queues on a system
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.EXPANDED
    id_display_name = 'SYSTEM_ID'

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        api_resource = '{0}/queues'.format(parsed_args.identifier)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, api_resource)
        # raise SystemError(self.requests_client.build_url())
        self.take_action_defaults(parsed_args)

        headers = SystemQueue().get_headers(verbosity_level=self.VERBOSITY)
        results = self.requests_client.get_data(params=self.post_payload)
        # raise SystemError(results)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
