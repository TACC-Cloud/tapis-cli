from tapis_cli.clients.http import HTTPFormatMany
from .bearer import TaccApisBearer
from ...mixins import (AppVerboseLevel, JsonVerbose, UploadJsonFile,
                       ServiceIdentifier)

__all__ = ['TaccApisFormatManyUnlimited', 'TaccApisFormatMany']


class TaccApisFormatManyUnlimited(JsonVerbose, HTTPFormatMany,
                                  TaccApisBearer):
    def get_parser(self, prog_name):
        parser = HTTPFormatMany.get_parser(self, prog_name)
        parser = HTTPFormatMany.add_common_parser_arguments(self, parser)
        parser = TaccApisBearer.add_common_parser_arguments(self, parser)
        return parser

    def before_take_action(self, parsed_args):
        self.init_clients(parsed_args)
        if self.app_verbose_level > 1:
            # raise SystemError(dir(self.app.options))
            parsed_args.formatter = 'json'
            if self.EXTRA_VERBOSITY is not None:
                self.VERBOSITY = self.EXTRA_VERBOSITY
        # self.take_action_defaults(parsed_args)
        return parsed_args


class TaccApisFormatMany(TaccApisFormatManyUnlimited):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        # Because this class is composed of multiple parents with get_parser
        # and add_common_parser_arguments methods, we call them in preferred
        # order because relying Python MRO will fail

        # print('TaccApisFormatMany.get_parser')
        parser = TaccApisFormatManyUnlimited.get_parser(self, prog_name)
        parser.add_argument('-l',
                            '--limit',
                            dest='limit',
                            default=36,
                            type=int,
                            help='Limit to L records')
        parser.add_argument('-o',
                            '--offset',
                            default=0,
                            dest='offset',
                            type=int,
                            help='Skip first O records')
        return parser

    def take_action_defaults(self, parsed_args):
        self.post_payload['limit'] = parsed_args.limit
        self.post_payload['offset'] = parsed_args.offset
        return self

        #     # raise SystemError(parsed_args)
        # # super().take_action(parsed_args)
        # # for requests made via AgavePy's swaggerpy client
        # # self.tapis_client = Agave.restore()
        # # # for requests made directly via requests module
        # # self.requests_client = Swaggerless(self.tapis_client)
        # return ((), ())
