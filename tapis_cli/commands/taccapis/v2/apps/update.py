from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from .create import AppsCreate

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsUpdate']


class AppsUpdate(AppsCreate, ServiceIdentifier):
    """Update an existing app
    """
    def get_parser(self, prog_name):
        parser = AppsCreate.get_parser(self, prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = AppsFormatOne.preprocess_args(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        headers = SearchableCommand.headers(self, App, parsed_args)

        rec = self.tapis_client.apps.update(appId=parsed_args.identifier,
                                            body=self.json_file_contents)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
