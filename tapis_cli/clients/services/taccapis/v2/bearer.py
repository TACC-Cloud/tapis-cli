from agavepy.agave import Agave
from .base import TaccApisCommandBase
import inspect

__all__ = ['TaccApisBearer', 'TaccApisNoBearer']


class TaccApisBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super().add_common_parser_arguments(parser)
        parser.add_argument('-z',
                            '--token',
                            dest='access_token',
                            metavar='<token>',
                            help="{0} {1}".format(self.constants.PLATFORM,
                                                  self.constants.ACCESS_TOKEN))
        return parser

    def init_clients(self, parsed_args):
        """Override CommandBase to set up client with passed token
        """
        client = Agave.restore()
        if parsed_args.access_token is not None:
            self.tapis_client = Agave(api_server=client.api_server,
                                      token=parsed_args.access_token)
        else:
            self.tapis_client = client
            self.tapis_client.token.refresh()
        self.requests_client = self._get_direct(self.tapis_client)
        return self


class TaccApisNoBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super().add_common_parser_arguments(parser)
        return parser
