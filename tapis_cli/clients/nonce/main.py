from ..http import HTTPFormatOne, HTTPFormatMany

__all__ = ['NonceHTTPFormatOne', 'NonceHTTPFormatMany']


def add_common_arguments(parser):
    parser.add_argument('--x-nonce',
                        dest='x_nonce',
                        type=str,
                        help="Tapis nonce")
    return parser


class NonceHTTPFormatOne(HTTPFormatOne):
    """HTTP+Nonce Record Display
    """
    def get_parser(self, prog_name):
        parser = super(NonceHTTPFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class NonceHTTPFormatMany(HTTPFormatMany):
    """HTTP+Nonce Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(NonceHTTPFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
