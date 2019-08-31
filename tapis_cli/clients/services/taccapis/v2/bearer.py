import argparse
import json
from agavepy.agave import Agave

from cliff.command import Command
from cliff.hooks import CommandHook
from cliff.app import App
from tapis_cli.display import Verbosity

from ....oauth import BearerTokenFormatOne, BearerTokenFormatMany
from .request import Swaggerless

__all__ = [
    'TaccApisBase', 'TaccApisFormatOne', 'TaccApisFormatMany',
    'AppVerboseLevel', 'JsonVerbose', 'UploadJsonFile',
    'TapisServiceIdentifier'
]


def add_common_arguments(parser):
    # parser.add_argument('-v',
    #                     dest='verbose',
    #                     action='store_true',
    #                     help='Verbose output (JSON)')
    return parser


class TaccApisBase(object):
    pass


class AppVerboseLevel(object):
    """Lets a client access the cliff App's verbosity level
    """
    VERBOSITY = None
    EXTRA_VERBOSITY = None

    @property
    def app_verbose_level(self):
        """Exposes the app-scoped verbosity level as a formatter property
        """
        vlevel = 1
        try:
            vlevel = self.app_args.verbose_level
        except Exception:
            pass
        return vlevel


class JsonVerbose(AppVerboseLevel):
    """Configures a client to use JSON as formatter when verbose is requested
    """
    EXTRA_VERBOSITY = Verbosity.RECORD

    @property
    def formatter_default(self):
        """Overrides formatter_default to return JSON when -v is passed
        """
        if self.app_verbose_level > 1:
            return 'json'
        else:
            return 'table'


class TapisServiceIdentifier(object):
    """Configures a client to expect a mandatory identifier
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        id_name = getattr(self, 'id_display_name', None)
        if id_name is not None:
            parser.add_argument('identifier',
                                type=str,
                                help=self.id_display_name)
        return parser


class TasApiClient(object):
    def init_clients(self):
        self.tapis_client = Agave.restore()
        # for requests made directly via requests module
        self.requests_client = Swaggerless(self.tapis_client)


class UploadJsonFile(object):
    """Configures a client to accept and load a JSON file
    """
    json_loaded = dict()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('-F',
                            '--file',
                            dest='json_file_name',
                            type=str,
                            help='JSON payload file')
        return parser

    def handle_file_upload(self, parsed_args):
        with open(parsed_args.json_file_name, 'rb') as jfile:
            payload = json.load(jfile)
            setattr(self, 'json_file_contents', payload)


class TaccApisFormatOne(JsonVerbose, TasApiClient, BearerTokenFormatOne):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        self.init_clients()
        return ((), ())
        # return super().take_action(parsed_args)


class TaccApisFormatMany(JsonVerbose, TasApiClient, BearerTokenFormatMany):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = add_common_arguments(parser)
        # if self.id_display_name is not None:
        #     parser.add_argument('identifier',
        #                         type=str,
        #                         help=self.id_display_name)
        parser.add_argument('-l',
                            '--limit',
                            dest='limit',
                            default=36,
                            type=int,
                            help='Limit to L records')
        parser.add_argument('-o',
                            '--offset',
                            default=0,
                            dest='offset',
                            type=int,
                            help='Skip first O records')
        return parser

    # @property
    # def formatter_default(self):
    #     """Overrides formatter_default to return JSON when -v is passed
    #     """
    #     if self.app_verbose_level > 1:
    #         return 'json'
    #     else:
    #         return 'table'

    def take_action(self, parsed_args):
        # This needs to be more sophisticated - does not allow overrides etc
        self.init_clients()
        if self.app_verbose_level > 1:
            # raise SystemError(dir(self.app.options))
            parsed_args.formatter = 'json'
            if self.EXTRA_VERBOSITY is not None:
                self.VERBOSITY = self.EXTRA_VERBOSITY
            # raise SystemError(parsed_args)
        # super().take_action(parsed_args)
        # for requests made via AgavePy's swaggerpy client
        # self.tapis_client = Agave.restore()
        # # for requests made directly via requests module
        # self.requests_client = Swaggerless(self.tapis_client)
        return ((), ())
