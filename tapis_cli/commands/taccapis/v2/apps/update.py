from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import AppIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from .create import AppsCreate

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsUpdate']


class AppsUpdate(AppsCreate, AppIdentifier):

    HELP_STRING = 'Update an existing App'
    LEGACY_COMMMAND_STRING = 'apps-addupdate'

    def get_parser(self, prog_name):
        parser = super(AppsUpdate, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        # Activates usage of argument from WorkingDirectoryArg
        self.set_working_directory(parsed_args)
        self.handle_file_upload(parsed_args)

        headers = self.render_headers(App, parsed_args)
        rec = self.tapis_client.apps.update(appId=app_id,
                                            body=self.json_file_contents)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
