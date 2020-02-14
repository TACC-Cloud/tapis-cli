from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from tapis_cli.display import Verbosity
from tapis_cli import et

from . import API_NAME, SERVICE_VERSION
from .models import Token
from .formatters import TokenFormatOne

__all__ = ['TokenRefresh']


class TokenRefresh(TokenFormatOne):
    """Refresh the current Tapis access token
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        # TODO - accept refresh token
        parser = super(TokenRefresh, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        parsed_args = super(TokenRefresh, self).preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = super(TokenRefresh, self).render_headers(Token, parsed_args)
        try:
            result = self.tapis_client.refresh()
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

        et.phone_home()
        return (tuple(headers), tuple(result))
