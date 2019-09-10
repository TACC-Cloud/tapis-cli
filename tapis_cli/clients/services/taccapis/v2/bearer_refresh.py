from .bearer import TaccApisOnlyBearer

__all__ = ['TaccApisBearerRefresh']


class TaccApisBearerRefresh(TaccApisOnlyBearer):
    """Base class for Tapis API commands both an access token and a refresh token
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisOnlyBearer,
                       self).add_common_parser_arguments(parser)
        parser.add_argument(
            '-z',
            '--refresh-token',
            dest='refresh_token',
            type=str,
            help="{0} {1}".format(self.constants.PLATFORM,
                                  self.constants.REFRESH_TOKEN))
        return parser
