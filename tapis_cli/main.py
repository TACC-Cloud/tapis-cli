import argparse
import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo

from . import __about__ as about
from . import settings

version_info = VersionInfo('dc_cli')

class Tapis_App(App):

    logger = logging.getLogger(__name__)
    if settings.LOGLEVEL is not None:
        logging.basicConfig(level=settings.LOGLEVEL)

    def __init__(self):
        super(Tapis_App, self).__init__(
            description=about.__project__,
            version=version_info.version_string(),
            command_manager=CommandManager('tapis.cli'),
            deferred_help=True,
        )

    # TODO - Add foundational options like tenant, sandbox, verify_ssl, etc
    def build_option_parser(self, description, version):
        parser = super(Tapis_App, self).build_option_parser(
            description, version)
        return parser

    def initialize_app(self, argv):
        super(Tapis_App, self).initialize_app(argv)
        self.logger.debug('Starting app, options: {}'.format(self.options))

def main(argv=sys.argv[1:]):
    catalogApp = Tapis_App()
    return catalogApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
