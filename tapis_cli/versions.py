import logging
from cliff.command import Command


# NOTE - This is a mockup.
# NOTE - Each api 'driver' will implement a version func, which will be called
class Version(Command):
    """Show API versions"""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.app.stdout.write('\n'.join([
            'Abaco: 1.3.0', 'Agave: 2.4.0-r9c8adc7', 'Aloe: 2.4.0-r9c8adc7',
            'Gitlab 11.4', 'Keys: 1.0.1', 'Registry: 2'
            'TAS: 1'
        ]))
