from .bearer import BearerTokenFormatOne, BearerTokenFormatMany

__all__ = ['ImpersonationTokenFormatOne', 'ImpersonationTokenFormatMany']


def add_common_arguments(parser):
    parser.add_argument('--impersonation-token',
                        type=str,
                        help="Impersonation bearer token")
    return parser


class ImpersonationTokenFormatOne(BearerTokenFormatOne):
    """HTTP+Bearer Record Display
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class ImpersonationTokenFormatMany(BearerTokenFormatMany):
    """HTTP+Bearer Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
