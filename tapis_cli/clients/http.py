import argparse
from cliff.display import DisplayCommandBase
from cliff.lister import Lister
from cliff.show import ShowOne

__all__ = ['HTTPFormatOne', 'HTTPFormatMany']


def add_common_arguments(parser):
    parser.add_argument(
        '-k',
        '--no-verify',
        dest='verify_ssl',
        action='store_false',
        help="Allow insecure server connections when using SSL")
    return parser


class HTTPFormatOne(ShowOne):
    """HTTP Record Display
    """
    def get_parser(self, prog_name):
        parser = super(HTTPFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class HTTPFormatMany(Lister):
    """HTTP Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(HTTPFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    # def run(self, parsed_args):
    #     raise SystemError(dir(self.formatter_default))
    #     #self.formatter_default = 'json'
    #     # setattr(self, 'formatter_default', 'json')
    #     return super(HTTPFormatMany, self).run(parsed_args)

    def take_action(self, parsed_args):
        return ((), ())
