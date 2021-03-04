from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

from .create import SystemsCreate

__all__ = ['SystemsUpdate']


class SystemsUpdate(SystemsCreate, ServiceIdentifier):

    HELP_STRING = 'Update an existing System'
    LEGACY_COMMMAND_STRING = 'systems-addupdate'

    def get_parser(self, prog_name):
        parser = SystemsCreate.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)
        self.update_json_creds(parsed_args)

        headers = headers = SearchableCommand.render_headers(
            self, System, parsed_args)
        rec = self.tapis_client.systems.update(systemId=parsed_args.identifier,
                                               body=self.json_file_contents)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
