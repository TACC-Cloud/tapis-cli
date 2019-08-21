from .bearer import BearerTokenFormatOne, BearerTokenFormatMany

__all__ = ['RefreshBearerTokenFormatOne', 'RefreshBearerTokenFormatMany']


def add_common_arguments(parser):
    parser.add_argument('--refresh-token',
                        type=str,
                        help="Tapis Oauth refresh token")
    return parser


class RefreshBearerTokenFormatOne(BearerTokenFormatOne):
    """HTTP+Bearer+Refresh Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(RefreshBearerTokenFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class RefreshBearerTokenFormatMany(BearerTokenFormatMany):
    """HTTP+Bearer+Refresh Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(RefreshBearerTokenFormatMany,
                       self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
