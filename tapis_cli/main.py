import argparse
import logging
import os
import sys

from colorama import init, deinit
from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo

from .__about__ import About
from . import PKG_NAME
from . import settings

from agavepy.agave import Agave

about_info = About(PKG_NAME)
version_info = VersionInfo(PKG_NAME)


class Tapis_App(App):
    def __init__(self):
        super(Tapis_App, self).__init__(
            description='{0}: {1}. For support contact {2}'.format(
                about_info.project, about_info.summary, about_info.help),
            version=version_info.version_string(),
            command_manager=CommandManager('tapis.cli'),
            deferred_help=True,
        )
        # Force table formatting to fit window width
        if settings.TAPIS_CLI_FIT_WIDTH:
            os.environ['CLIFF_FIT_WIDTH'] = '1'

    def prepare_to_run_command(self, cmd):
        """Prepares to run the command

        Checks if the minimal parameters are provided and creates the
        client interface.
        This is inherited from the framework.
        """
        self.configure_logging()

    def configure_logging(self):
        """Create logging handlers for any log output."""

        try:    # Python 2.7
            from logging import NullHandler
        except ImportError:

            class NullHandler(logging.Handler):
                def emit(self, record):
                    pass

        logging.getLogger('stevedore.extension').setLevel(logging.WARNING)
        logging.getLogger(__name__).setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(NullHandler())

        # if settings.TAPIS_CLI_LOG_LEVEL is not None:
        #     logging.basicConfig(level=settings.TAPIS_CLI_LOG_LEVEL)
        return

    # TODO - Add foundational options like tenant, sandbox, verify_ssl, etc
    def build_option_parser(self, description, version):
        parser = super(Tapis_App,
                       self).build_option_parser(description, version)
        return parser

    def initialize_app(self, argv):
        super(Tapis_App, self).initialize_app(argv)
        self.logger.debug('Starting app, options: {}'.format(self.options))


def main(argv=sys.argv[1:]):
    init(autoreset=True)
    catalogApp = Tapis_App()
    # Swap out built-in complete for one that does not conflict with search commnds
    del catalogApp.command_manager.commands['complete']
    deinit()
    return catalogApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
