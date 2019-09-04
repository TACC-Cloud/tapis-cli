from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import UploadJsonFile, ServiceIdentifier
from .create import AppsCreate

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsUpdate']


class AppsUpdate(UploadJsonFile, ServiceIdentifier, AppsFormatOne):
    """Update an existing app
    """
    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = App().get_headers(self.VERBOSITY, parsed_args.formatter)
        self.handle_file_upload(parsed_args)

        rec = self.tapis_client.apps.update(appId=parsed_args.identifier,
                                            body=self.json_file_contents)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
