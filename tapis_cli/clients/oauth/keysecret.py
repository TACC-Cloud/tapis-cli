from ..http import HTTPFormatOne, HTTPFormatMany
from ..basic import BasicHTTPFormatOne, BasicHTTPFormatMany

__all__ = [
    'KeySecretBasicFormatOne', 'KeySecretBasicFormatMany',
    'KeySecretOnlyFormatOne', 'KeySecretOnlyFormatMany'
]


def add_common_arguments(parser):
    parser.add_argument('--client-key', type=str, help="Oauth client key")
    parser.add_argument('--client-secret',
                        type=str,
                        help="Oauth client secret")
    return parser


class KeySecretBasicFormatOne(BasicHTTPFormatOne):
    """HTTP+KeySecret+Basic Record Display
    """
    def get_parser(self, prog_name):
        parser = super(KeySecretBasicFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class KeySecretBasicFormatMany(BasicHTTPFormatMany):
    """HTTP+KeySecret+Basic Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(KeySecretBasicFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class KeySecretOnlyFormatOne(HTTPFormatOne):
    """HTTP+KeySecret Only Record Display
    """
    def get_parser(self, prog_name):
        parser = super(KeySecretOnlyFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class KeySecretOnlyFormatMany(HTTPFormatMany):
    """HTTP+KeySecret+Basic Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(KeySecretOnlyFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
