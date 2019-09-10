from ..http import HTTPFormatOne, HTTPFormatMany
from .keysecret import KeySecretFormatOne, KeySecretFormatMany

__all__ = [
    'BearerTokenFormatOne', 'BearerTokenFormatMany',
    'BearerTokenCreateFormatOne'
]


def add_common_arguments(parser):
    parser.add_argument('-z',
                        '--access-token',
                        dest='access_token',
                        type=str,
                        help="Oauth access token")
    parser.add_argument('-H',
                        '--api-server',
                        dest='api_server',
                        type=str,
                        help="API server base URL")
    return parser


class BearerTokenFormatOne(HTTPFormatOne):
    """HTTP+Bearer Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class BearerTokenCreateFormatOne(HTTPFormatOne, KeySecretFormatOne):
    """HTTP+Bearer Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class BearerTokenFormatMany(HTTPFormatMany):
    """HTTP+Bearer Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
