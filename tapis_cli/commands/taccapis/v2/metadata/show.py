from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.taccapis.v2.bearer import TapisServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne

__all__ = ['MetadataShow']


class MetadataShow(TapisServiceIdentifier, MetadataFormatOne):
    """Show a single metadata record
    """
    VERBOSITY = Verbosity.RECORD

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = Metadata().get_headers(self.VERBOSITY, parsed_args.formatter)

        rec = self.tapis_client.meta.getMetadata(uuid=parsed_args.identifier)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
