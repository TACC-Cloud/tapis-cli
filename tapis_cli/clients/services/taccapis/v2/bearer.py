from agavepy.agave import Agave
from ....oauth import BearerTokenFormatOne, BearerTokenFormatMany
from .requests import Swaggerless

__all__ = ['TaccApisBase', 'TaccApisFormatOne', 'TaccApisFormatMany']


def add_common_arguments(parser):
    return parser


class TaccApisBase(object):
    id_display_name = None


class TaccApisFormatOne(TaccApisBase, BearerTokenFormatOne):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        if self.id_display_name is not None:
            parser.add_argument('identifer',
                                type=str,
                                help=self.id_display_name)
        return parser

    def take_action(self, parsed_args):
        # This needs to be more sophisticated - does not allow overrides etc
        super().take_action(parsed_args)
        self.taccapi_client = Agave.restore()
        return ((), ())


class TaccApisFormatMany(TaccApisBase, BearerTokenFormatMany):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        parser.add_argument('-l',
                            '--limit',
                            dest='limit',
                            default=100,
                            type=int,
                            help='Limit to n records')
        parser.add_argument('-s',
                            '--skip',
                            default=0,
                            dest='offset',
                            type=int,
                            help='Skip first n records')
        return parser

    def take_action(self, parsed_args):
        # This needs to be more sophisticated - does not allow overrides etc
        super().take_action(parsed_args)
        # for requests made via AgavePy's swaggerpy client
        self.tapis_client = Agave.restore()
        # for requests made directly via requests module
        self.requests_client = Swaggerless(self.tapis_client)
        return ((), ())
