import inspect
from agavepy.agave import Agave, AgaveError
from .base import TaccApisCommandBase
from tapis_cli import constants, settings

__all__ = ['TaccApisBearer', 'TaccApisNoBearer']


class TaccApisBearer(TaccApisCommandBase):

    ACCEPT_ACCESS_TOKEN = True
    ACCEPT_REFRESH_TOKEN = False
    ACCEPT_NONCE = False
    ALLOW_NO_VERIFY = True

    def add_common_parser_arguments(self, parser):

        parser = super(TaccApisBearer,
                       self).add_common_parser_arguments(parser)

        g = parser.add_argument_group('auth override')

        g.add_argument('-H',
                       '--api-server',
                       dest='api_server',
                       metavar='URL',
                       help="{0} {1}".format(constants.PLATFORM,
                                             constants.API_SERVER))

        if self.ACCEPT_ACCESS_TOKEN:
            g.add_argument('-z',
                           '--token',
                           dest='access_token',
                           metavar='TOKEN',
                           help="{0} {1}".format(constants.PLATFORM,
                                                 constants.ACCESS_TOKEN))

        if self.ACCEPT_NONCE:
            g.add_argument('-Z',
                           '--nonce',
                           dest='nonce',
                           metavar='NONCE',
                           help="{0} {1}".format(constants.PLATFORM,
                                                 constants.NONCE))

        if self.ALLOW_NO_VERIFY:
            g.add_argument('--no-verify',
                           dest='verify_ssl',
                           action='store_false',
                           default=settings.TAPIS_CLI_VERIFY_SSL,
                           help="Allow insecure SSL connections")
        return parser

    def init_clients(self, parsed_args):
        """Override CommandBase to set up client with passed token
        """

        api_server = getattr(parsed_args, 'api_server', None)
        token = getattr(parsed_args, 'access_token', None)
        nonce = getattr(parsed_args, 'nonce', None)
        verify_ssl = getattr(parsed_args, 'verify_ssl', True)

        if (token is not None or nonce is not None) and api_server is None:
            try:
                client = Agave._read_current(agave_kwargs=True)
                api_server = client['api_server']
            except Exception:
                raise AgaveError('Unable to discover Tapis API server URL.')

        # Initialize the AgavePy client
        try:
            if api_server is not None and token is not None:
                self.tapis_client = Agave(api_server=api_server,
                                          token=token,
                                          verify=verify_ssl)
            elif api_server is not None and nonce is not None:
                self.tapis_client = Agave(api_server=api_server,
                                          use_nonce=True,
                                          verify=verify_ssl)
                self.client_extra_args['nonce'] = nonce
            else:

                # Load from disk cache
                # client = Agave.restore()
                clients = Agave._read_clients()
                client0 = clients[0]
                # Override SSL verification from stored client
                client0['verify'] = verify_ssl
                client = Agave(**client0)

                self.tapis_client = client
                self.tapis_client.refresh()

        except Exception:
            raise AgaveError(constants.TAPIS_AUTH_FAIL)

        # Initialize the direct requests client
        try:
            # Direct client will inherit SSL check behavior from Tapis client
            self.requests_client = self._get_direct(self.tapis_client)
        except Exception:
            raise AgaveError(constants.TAPIS_AUTH_FAIL)

        return self


class _TaccApisBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisBearer,
                       self).add_common_parser_arguments(parser)
        g = parser.add_argument_group('auth override')
        g.add_argument('-H',
                       '--api-server',
                       dest='api_server',
                       metavar='URL',
                       help="{0} {1}".format(constants.PLATFORM,
                                             constants.API_SERVER))
        g.add_argument('-z',
                       '--token',
                       dest='access_token',
                       metavar='TOKEN',
                       help="{0} {1}".format(constants.PLATFORM,
                                             constants.ACCESS_TOKEN))
        g.add_argument('--no-verify',
                       dest='verify_ssl',
                       action='store_false',
                       help="Allow insecure SSL connections")
        return parser

    def init_clients(self, parsed_args):
        """Override CommandBase to set up client with passed token
        """
        # client = Agave.restore()
        if parsed_args.api_server is not None and parsed_args.access_token is not None:
            self.tapis_client = Agave(api_server=parsed_args.api_server,
                                      token=parsed_args.access_token)
        elif parsed_args.access_token is not None:
            try:
                client = Agave._read_current(agave_kwargs=True)
            except Exception:
                raise AgaveError(
                    'Tapis API server was not discoverable. Exiting.')
            self.tapis_client = Agave(api_server=client['api_server'],
                                      token=parsed_args.access_token)
        else:
            try:
                client = Agave.restore()
                self.tapis_client = client
                self.tapis_client.refresh()
                # self.requests_client = self._get_direct(self.tapis_client)
            except Exception:
                raise AgaveError(constants.TAPIS_AUTH_FAIL)

        try:
            self.requests_client = self._get_direct(self.tapis_client)
        except Exception:
            raise AgaveError(constants.TAPIS_AUTH_FAIL)

        return self


class TaccApisNoBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisNoBearer,
                       self).add_common_parser_arguments(parser)
        return parser
