import inspect
from agavepy.agave import Agave, AgaveError
from .base import TaccApisCommandBase
from tapis_cli import constants

__all__ = ['TaccApisBearer', 'TaccApisNoBearer']


class TaccApisBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisBearer,
                       self).add_common_parser_arguments(parser)
        g = parser.add_argument_group('auth override')
        g.add_argument('-H',
                       '--api-server',
                       dest='api_server',
                       metavar='<url>',
                       help="{0} {1}".format(self.constants.PLATFORM,
                                             self.constants.API_SERVER))
        g.add_argument('-z',
                       '--token',
                       dest='access_token',
                       metavar='<token>',
                       help="{0} {1}".format(self.constants.PLATFORM,
                                             self.constants.ACCESS_TOKEN))
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
