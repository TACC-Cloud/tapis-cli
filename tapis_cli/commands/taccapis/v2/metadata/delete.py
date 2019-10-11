from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne
from .mixins import MetadataIdentifier

__all__ = ['MetadataDelete']


class MetadataDelete(MetadataFormatOne, MetadataIdentifier):
    """Delete a Metadata record by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = MetadataFormatOne.get_parser(self, prog_name)
        parser = MetadataIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = MetadataFormatOne.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.take_action_defaults(parsed_args)
        identifier = parsed_args.identifier
        self.validate_identifier(identifier)

        deleted = []
        exceptions = []
        try:
            self.tapis_client.meta.deleteMetadata(uuid=parsed_args.identifier)
            deleted.append(parsed_args.identifier)
        except Exception as err:
            exceptions.append(err)

        # Following the example set for file upload/download, report
        # summary statistics in table or structured form if showing yaml/json
        #
        # Considering implementing a plural version of ServiceIdentifer to
        # allow commands to process multiple IDs - most useful for batch delete
        headers = ['deleted', 'messages']
        if parsed_args.formatter in ('json', 'yaml'):
            data = [deleted, [str(e) for e in exceptions]]
        else:
            data = [len(deleted), len(exceptions)]
        return (tuple(headers), tuple(data))
