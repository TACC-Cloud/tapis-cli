"""Basic HTTP requests client
"""
import argparse
from cliff.display import DisplayCommandBase
from cliff.lister import Lister
from cliff.show import ShowOne
from tapis_cli import constants

__all__ = ['HTTPFormatOne', 'HTTPFormatMany']


class HTTPCommandBase(object):
    """A base class for building HTTP-based comands
    """
    constants = constants

    def get_parser(self, prog_name):
        pass

    def take_action(self, parsed_args):
        pass

    def add_common_parser_arguments(self, parser):
        # Derived classes must call the parent's super()
        # print('HTTPCommandBase')
        return parser


class HTTPFormatOne(ShowOne, HTTPCommandBase):
    """HTTP Single Record Display
    """

    # def get_parser(self, prog_name):
    #     # Child classes must call super() to inherit this
    #     parser = super(HTTPFormatOne, self).get_parser(prog_name)
    #     parser = self.add_common_parser_arguments(parser)
    #     return parser


class HTTPFormatMany(Lister, HTTPCommandBase):
    """HTTP Records Listing
    """
    # def get_parser(self, prog_name):
    #     parser = super(HTTPFormatMany, self).get_parser(prog_name)
    #     parser = self.add_common_parser_arguments(parser)
    #     return parser
