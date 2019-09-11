import argparse
import datetime
import json
from agavepy.agave import Agave

from cliff.command import Command
from cliff.hooks import CommandHook
from cliff.app import App
from tapis_cli.display import Verbosity
from tapis_cli.utils import datetime_to_isodate, datetime_to_human
from .apiclient import TaccApiClient

from ...mixins import (AppVerboseLevel, JsonVerbose, UploadJsonFile,
                       ServiceIdentifier)
from ....oauth import (BearerTokenFormatOne, BearerTokenFormatMany,
                       RefreshBearerTokenFormatOne)

__all__ = [
    'TaccApisBase', 'TaccApisFormatOne', 'TaccApisFormatMany',
    'TaccApisFormatManyUnlimited', 'TaccApisWithRefreshFormatOne'
]


def add_common_arguments(parser):
    # parser.add_argument('-v',
    #                     dest='verbose',
    #                     action='store_true',
    #                     help='Verbose output (JSON)')
    return parser


class TaccApisBase(object):
    # The contents of a search payload can be loaded in here for use
    # by the Swaggerless API client
    post_payload = dict()

    def take_action_defaults(self, parsed_args):
        return self

    def render_value(self, value):
        """Renders a value basd on current display format

        Each field value in a response can be passed through this function
        to implement format-specific rendering
        """
        # If the value is a date/time and display is a table, render as
        # a human-readable value instead of an ISO-8601 date
        if isinstance(value, datetime.datetime):
            if self.formatter_default == 'table':
                # TODO - figure out why this only works for the ShowOne
                value = datetime_to_human(value)
            else:
                value = datetime_to_isodate(value)
        return value


class TaccApisFormatOne(JsonVerbose, TaccApiClient, BearerTokenFormatOne):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        self.init_clients(parsed_args)
        return ((), ())
        # return super().take_action(parsed_args)


class TaccApisWithRefreshFormatOne(TaccApisFormatOne,
                                   RefreshBearerTokenFormatOne):
    pass


class TaccApisFormatMany(JsonVerbose, TaccApiClient, BearerTokenFormatMany):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = add_common_arguments(parser)
        # if self.service_id_type is not None:
        #     parser.add_argument('identifier',
        #                         type=str,
        #                         help=self.service_id_type)
        parser.add_argument('-l',
                            '--limit',
                            dest='limit',
                            default=36,
                            type=int,
                            help='Limit to LL records')
        parser.add_argument('-o',
                            '--offset',
                            default=0,
                            dest='offset',
                            type=int,
                            help='Skip first OO records')
        return parser

    def take_action_defaults(self, parsed_args):
        super().take_action_defaults(parsed_args)
        self.post_payload['limit'] = parsed_args.limit
        self.post_payload['offset'] = parsed_args.offset
        return self

    def take_action(self, parsed_args):
        # This needs to be more sophisticated - does not allow overrides etc
        self.init_clients(parsed_args)
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


class TaccApisFormatManyUnlimited(TaccApisFormatMany):
    def get_parser(self, prog_name):
        parser = BearerTokenFormatMany.get_parser(self, prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action_defaults(self, parsed_args):
        return self
