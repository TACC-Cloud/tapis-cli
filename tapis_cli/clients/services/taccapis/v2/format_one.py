from tapis_cli.clients.http import HTTPFormatOne
from .bearer import TaccApisBearer
from ...mixins import (AppVerboseLevel, JsonVerbose, UploadJsonFile,
                       ServiceIdentifier)


class TaccApisFormatOne(JsonVerbose, HTTPFormatOne, TaccApisBearer):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        # Because this class is composed of multiple parents with get_parser
        # and add_common_parser_arguments methods, we call them in preferred
        # order because relying Python MRO will fail
        #
        # print('TaccApisFormatOne.get_parser')
        parser = HTTPFormatOne.get_parser(self, prog_name)
        parser = HTTPFormatOne.add_common_parser_arguments(self, parser)
        parser = TaccApisBearer.add_common_parser_arguments(self, parser)
        return parser

    def take_action_defaults(self, parsed_args):
        return self

    def before_take_action(self, parsed_args):
        self.init_clients(parsed_args)
        parsed_args = super().before_take_action(parsed_args)
        self.take_action_defaults(parsed_args)
        return parsed_args


class TaccApisFormatOneNoBearer(JsonVerbose, HTTPFormatOne):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        # Because this class is composed of multiple parents with get_parser
        # and add_common_parser_arguments methods, we call them in preferred
        # order because relying Python MRO will fail
        #
        # print('TaccApisFormatOne.get_parser')
        parser = HTTPFormatOne.get_parser(self, prog_name)
        parser = HTTPFormatOne.add_common_parser_arguments(self, parser)
        return parser

    def take_action_defaults(self, parsed_args):
        return self

    def before_take_action(self, parsed_args):
        self.init_clients(parsed_args)
        parsed_args = super().before_take_action(parsed_args)
        self.take_action_defaults(parsed_args)
        return parsed_args
