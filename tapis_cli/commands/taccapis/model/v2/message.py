"""Data model for a message-only response
"""
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from tapis_cli import constants
from . import TapisModel

__all__ = ['Message']


class Message(TapisModel):
    """Model of a Tapis message-only response
    """

    SEARCH_ARGS = []

    def get_headers(self, verbosity_level=1, formatter='table'):
        """Custom headers for Message
        """
        return ['message', 'warning']
