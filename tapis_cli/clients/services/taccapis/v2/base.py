from tapis_cli import constants
from .apiclient import TaccApiClient
from ...mixins import (AppVerboseLevel, JsonVerbose, UploadJsonFile,
                       ServiceIdentifier)

__all__ = ['TaccApisCommandBase']


class TaccApisCommandBase(TaccApiClient):
    """A base class for building Tapis API client commands
    """
    constants = constants
    post_payload = {}
    # Extra args that can be passed as **dict to all requests
    client_extra_args = {}

    def add_common_parser_arguments(self, parser):
        # print('TaccApisCommandBase.add_common_parser_arguments')
        # Derived classes must call the parent's super()
        return parser

    def get_parser(self, prog_name):
        # Derived classes must call the parent's super()
        parser = super(TaccApisCommandBase, self).get_parser(prog_name)
        parser = self.add_common_parser_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        # Derived classes must call the parent's super()
        self.init_clients(parsed_args)
        return ((), ())

    def update_payload(self, parsed_args):
        return self
