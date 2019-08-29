"""Mockup formatters
"""
import argparse
from cliff.lister import Lister
from cliff.show import ShowOne

__all__ = ['FormatOne', 'FormatMany']


class FormatOne(ShowOne):
    """Generic Record Display
    """
    def get_parser(self, prog_name):
        parser = super(FormatOne, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class FormatMany(Lister):
    """Generic Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(FormatMany, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
