from agavepy.agave import AgaveError
from tapis_cli.clients.http import HTTPFormatOne
from .bearer import TaccApisBearer
from ...mixins import (AppVerboseLevel, JsonVerbose, UploadJsonFile,
                       ServiceIdentifier, LegacyCommmandHelp)


class TaccApisFormatOne(LegacyCommmandHelp, JsonVerbose, HTTPFormatOne,
                        TaccApisBearer):
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

    def update_payload(self, parsed_args):
        return self

    def preprocess_args(self, parsed_args):
        # try:
        self.init_clients(parsed_args)
        # except Exception:
        # raise AgaveError("Failed to load Tapis API client. Run 'tapis auth init [--interactive]' to resolve this.")
        parsed_args = super(TaccApisFormatOne,
                            self).preprocess_args(parsed_args)
        self.update_payload(parsed_args)
        return parsed_args


class TaccApisFormatOneNoBearer(LegacyCommmandHelp, JsonVerbose,
                                HTTPFormatOne):
    def get_parser(self, prog_name):
        # Because this class is composed of multiple parents with get_parser
        # and add_common_parser_arguments methods, we call them in preferred
        # order because relying Python MRO will fail
        #
        # print('TaccApisFormatOne.get_parser')
        parser = HTTPFormatOne.get_parser(self, prog_name)
        parser = HTTPFormatOne.add_common_parser_arguments(self, parser)
        return parser

    def update_payload(self, parsed_args):
        return self

    def preprocess_args(self, parsed_args):
        # try:
        self.init_clients(parsed_args)
        # except Exception:
        # raise AgaveError("Failed to load Tapis API client. Run 'tapis auth init [--interactive]' to resolve this.")
        parsed_args = super(TaccApisFormatOneNoBearer,
                            self).preprocess_args(parsed_args)
        self.update_payload(parsed_args)
        return parsed_args
