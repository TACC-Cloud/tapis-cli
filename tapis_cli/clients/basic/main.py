from ..http import HTTPFormatOne, HTTPFormatMany

__all__ = ['BasicHTTPFormatOne', 'BasicHTTPFormatMany']


def add_common_arguments(parser):
    parser.add_argument('--username',
                        dest='username',
                        type=str,
                        help="Username")
    parser.add_argument('--password',
                        dest='password',
                        type=str,
                        help="Password")
    return parser


class BasicHTTPFormatOne(HTTPFormatOne):
    """HTTP+Basic Record Display
    """
    def get_parser(self, prog_name):
        parser = super(BasicHTTPFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class BasicHTTPFormatMany(HTTPFormatMany):
    """HTTP+Basic Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(BasicHTTPFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
