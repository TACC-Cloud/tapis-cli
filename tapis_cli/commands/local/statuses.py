import logging
from cliff.command import Command


# NOTE - This is a mockup.
# NOTE - Each api 'driver' will implement a status func, which will be called
# NOTE - Response will be something like <Keyword> <Message>
class Status(Command):
    """Show API statuses"""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.app.stdout.write('\n'.join([
            'Abaco: Operational', 'Agave: Operational', 'Aloe: Operational',
            'Gitlab: Operational', 'Keys: Operational',
            'Registry: Operational', 'TAS: Operational'
        ]))
