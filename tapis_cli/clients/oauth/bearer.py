from ..http import HTTPFormatOne, HTTPFormatMany

__all__ = ['BearerTokenFormatOne', 'BearerTokenFormatMany']


def add_common_arguments(parser):
    parser.add_argument('-z',
                        '--access-token',
                        dest='access_token',
                        metavar='TOKEN',
                        type=str,
                        help="Oauth access token")
    parser.add_argument('-H',
                        '--api-server',
                        dest='api_server',
                        metavar='URI',
                        type=str,
                        help="API server")
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


class BearerTokenFormatMany(HTTPFormatMany):
    """HTTP+Bearer Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
