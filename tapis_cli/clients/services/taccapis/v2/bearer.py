from agavepy.agave import Agave
from cliff.app import App
from ....oauth import BearerTokenFormatOne, BearerTokenFormatMany
from .requests import Swaggerless

__all__ = ['TaccApisBase', 'TaccApisFormatOne', 'TaccApisFormatMany']


def add_common_arguments(parser):
    # parser.add_argument('-v',
    #                     dest='verbose',
    #                     action='store_true',
    #                     help='Verbose output (JSON)')
    return parser


class TaccApisBase(object):
    VERBOSITY = None
    EXTRA_VERBOSITY = None


class TaccApisFormatOne(BearerTokenFormatOne):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        if self.id_display_name is not None:
            parser.add_argument('identifier',
                                type=str,
                                help=self.id_display_name)
        return parser

    @property
    def formatter_default(self):
        """Overrides formatter_default to return JSON when -v is passed
        """
        if self.app_args.verbose_level > 1:
            return 'json'
        else:
            return 'table'

    def take_action(self, parsed_args):
        # This needs to be more sophisticated - does not allow overrides etc
        super().take_action(parsed_args)
        # for requests made via AgavePy's swaggerpy client
        self.tapis_client = Agave.restore()
        # for requests made directly via requests module
        self.requests_client = Swaggerless(self.tapis_client)
        return ((), ())


class TaccApisFormatMany(BearerTokenFormatMany):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        if self.id_display_name is not None:
            parser.add_argument('identifier',
                                type=str,
                                help=self.id_display_name)
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

    @property
    def formatter_default(self):
        """Overrides formatter_default to return JSON when -v is passed
        """
        if self.app_args.verbose_level > 1:
            return 'json'
        else:
            return 'table'

    def take_action(self, parsed_args):
        # This needs to be more sophisticated - does not allow overrides etc
        if self.app.options.verbose_level > 1:
            # raise SystemError(dir(self.app.options))
            parsed_args.formatter = 'json'
            if self.EXTRA_VERBOSITY is not None:
                self.VERBOSITY = self.EXTRA_VERBOSITY
            # raise SystemError(parsed_args)
        super().take_action(parsed_args)
        # for requests made via AgavePy's swaggerpy client
        self.tapis_client = Agave.restore()
        # for requests made directly via requests module
        self.requests_client = Swaggerless(self.tapis_client)
        return ((), ())
