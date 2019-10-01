import getpass
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis import SearchableCommand
from tapis_cli.constants import PLATFORM
from tapis_cli.utils import (fmtcols, prompt, get_hostname, get_public_ip,
                             get_local_username)

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
        parser = CreateTokenFormatOne.get_parser(self, prog_name)
        # TODO - This should be a mix-in
        parser.add_argument('--password',
                            dest='tapis_password',
                            help='{0} password'.format(PLATFORM))

        parser.add_argument(
            '--token-username',
            dest='token_username',
            help=
            'Username to impersonate with the returned token (requires admin privileges)'
        )
        return parser

    def take_action(self, parsed_args):
        parsed_args = CreateTokenFormatOne.before_take_action(
            self, parsed_args)
        self.take_action_defaults(parsed_args)

        # Allow prompt for password when not specified
        passwd = parsed_args.tapis_password
        if passwd is None:
            passwd = prompt('Password', passwd, secret=True)

        headers = SearchableCommand.headers(self, Token, parsed_args)
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
                headers.remove('expires_at')
                for h in headers:
                    # DERP
                    result.append(resp.get(h))
        except HTTPError as h:
            if str(h).startswith('400'):
                raise AgaveError(
                    'Failed to create a token pair: {0}'.format(h))
            else:
                raise AgaveError(str(h))
        # result = list()
        # for h in headers:
        #     # DERP
        #     result.append(self.tapis_client.token.token_info.get(h))
        return (tuple(headers), tuple(result))
