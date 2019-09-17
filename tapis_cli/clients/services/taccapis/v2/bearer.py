from .base import TaccApisCommandBase

__all__ = ['TaccApisNoBearer']


class TaccApisBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super().add_common_parser_arguments(parser)
        parser.add_argument('-z',
                            '--token',
                            dest='access_token',
                            type=str,
                            help="{0} {1}".format(self.constants.PLATFORM,
                                                  self.constants.ACCESS_TOKEN))
        return parser


class TaccApisNoBearer(TaccApisCommandBase):
    """Base class for Tapis API commands that accept only an access token
    """
    def add_common_parser_arguments(self, parser):
        parser = super().add_common_parser_arguments(parser)
        return parser
