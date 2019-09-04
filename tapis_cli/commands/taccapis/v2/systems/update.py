from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import UploadJsonFile, ServiceIdentifier
from .create import SystemsCreate

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsUpdate']


class SystemsUpdate(UploadJsonFile, ServiceIdentifier, SystemsFormatOne):
    """Update an existing system
    """
    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = System().get_headers(self.VERBOSITY, parsed_args.formatter)
        self.handle_file_upload(parsed_args)

        rec = self.tapis_client.systems.update(systemId=parsed_args.identifier,
                                               body=self.json_file_contents)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
