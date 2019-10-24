import getpass
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from tapis_cli.display import Verbosity
from tapis_cli.constants import PLATFORM
from tapis_cli.utils import (fmtcols, prompt, get_hostname, get_public_ip,
                             get_local_username, fg_green, fg_bright)
from tapis_cli import et

from . import API_NAME, SERVICE_VERSION
from .models import Token
from .formatters import CreateTokenFormatOne

__all__ = ['TokenCreate']


class TokenCreate(CreateTokenFormatOne):
    """Create a new Tapis access/refresh token pair
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(TokenCreate, self).get_parser(prog_name)
        # TODO - This should be a mix-in
        parser.add_argument('--password',
                            dest='tapis_password',
                            help='{0} password'.format(PLATFORM))

        parser.add_argument(
            '--token-username',
            dest='token_username',
            help='Impersonation username (requires admin privileges)')
        return parser

    def take_action(self, parsed_args):
        parsed_args = super(TokenCreate, self).preprocess_args(parsed_args)
        self.update_payload(parsed_args)

        # Allow prompt for password when not specified
        passwd = parsed_args.tapis_password
        if passwd is None:
            passwd = prompt('Password', passwd, secret=True)

        headers = super(TokenCreate, self).render_headers(Token, parsed_args)
        self.tapis_client.token.password = passwd

        result = list()
        try:
            if parsed_args.token_username is None:
                resp = self.tapis_client.token.create()
                self.tapis_client.token.password = None
                for h in headers:
                    # DERP
                    result.append(self.tapis_client.token.token_info.get(h))
            else:
                self.requests_client.setup(API_NAME, None)
                data = {
                    'token_username': parsed_args.token_username,
                    'username': self.tapis_client.username,
                    'password': passwd,
                    'scope': 'PRODUCTION',
                    'grant_type': 'admin_password'
                }
                resp = self.requests_client.post_data_basic(data)
                # Not returned by service
                headers.remove('expires_at')
                # Do not return - we want impersonation tokens to expire
                headers.remove('refresh_token')
                for h in headers:
                    # DERP
                    result.append(resp.get(h))

                # Manually insert token username into response
                headers.append('username')
                # Nice feature - highlight the username
                result.append(parsed_args.token_username)

        except HTTPError as h:
            if str(h).startswith('400'):
                raise AgaveError(
                    'Failed to create a token pair: {0}'.format(h))
            else:
                raise AgaveError(str(h))

        et.phone_home()
        return (tuple(headers), tuple(result))
