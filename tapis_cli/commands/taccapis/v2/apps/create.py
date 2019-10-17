from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import UploadJsonFile
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsCreate']

# TODO - enforce use of create vs update by checking for existence of appId


class AppsCreate(UploadJsonFile, AppsFormatOne):
    """Create a new app
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(AppsCreate, self).get_parser(prog_name)
        parser = UploadJsonFile.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        headers = self.render_headers(App, parsed_args)
        rec = self.tapis_client.apps.add(body=self.json_file_contents)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
