import argparse
from cliff.display import DisplayCommandBase
from cliff.lister import Lister
from cliff.show import ShowOne

__all__ = ['HTTPFormatOne', 'HTTPFormatMany']

def add_common_arguments(parser):
    parser.add_argument(
        '--verify',
        dest='verify_ssl',
        type=bool,
        help="Verify SSL certificates"
    )
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

    def take_action(self, parsed_args):
        return ((), ())
