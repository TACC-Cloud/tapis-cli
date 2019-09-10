from ....basic import BasicHTTPFormatOne, BasicHTTPFormatMany
from .apiclient import TaccApiClient

__all__ = ['TaccApisBasicFormatOne', 'TaccBasicApisFormatMany']


def add_common_arguments(parser):
    return parser


class TaccApisBasicFormatOne(BasicHTTPFormatOne, TaccApiClient):
    """TACC APIs HTTP+Basic Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisBasicFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        self.init_clients(parsed_args)
        return ((), ())


class TaccBasicApisFormatMany(BasicHTTPFormatMany, TaccApiClient):
    """TACC APIs HTTP+Basic Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(TaccBasicApisFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        self.init_clients(parsed_args)
        return ((), ())
