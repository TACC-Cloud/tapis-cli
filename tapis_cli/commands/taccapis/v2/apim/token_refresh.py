from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import SERVICE_VERSION
from .models import Token
from .formatters import TokenFormatOne

__all__ = ['TokenRefresh']


class TokenRefresh(TokenFormatOne):
    """Refresh the current Tapis access token
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = Token().get_headers(self.VERBOSITY, parsed_args.formatter)
        try:
            result = self.tapis_client.token.refresh()
        except HTTPError as h:
            if str(h).startswith('400'):
                raise AgaveError(
                    'Failed to refresh token. Try "tapis sessions token create"'
                )
            else:
                raise AgaveError(str(h))
        result = list()
        for h in headers:
            result.append(self.tapis_client.token.token_info.get(h))
        return (tuple(headers), tuple(result))
