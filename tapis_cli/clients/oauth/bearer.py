from .keysecret import KeySecretOnlyFormatOne, KeySecretOnlyFormatMany

__all__ = ['BearerTokenFormatOne', 'BearerTokenFormatMany']

def add_common_arguments(parser):
    parser.add_argument(
        '--access-token',
        type=str,
        help="Tapis Oauth access token"
    )
    return parser

class BearerTokenFormatOne(KeySecretOnlyFormatOne):
    """HTTP+Bearer Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())

class BearerTokenFormatMany(KeySecretOnlyFormatMany):
    """HTTP+Bearer Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(BearerTokenFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
