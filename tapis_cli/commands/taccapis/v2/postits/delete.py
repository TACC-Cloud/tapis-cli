from tapis_cli.display import Verbosity

from . import API_NAME, SERVICE_VERSION
from .mixins import PostItsIdentifier
from .models import PostIt, HTTP_METHODS, DEFAULT_LIFETIME, DEFAULT_MAX_USES
from .formatters import PostItsFormatOne

__all__ = ['PostItsDelete']


class PostItsDelete(PostItsFormatOne, PostItsIdentifier):

    HELP_STRING = 'Delete a Postit'
    LEGACY_COMMMAND_STRING = 'postits-delete'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(PostItsDelete, self).get_parser(prog_name)
        parser = PostItsIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        identifier = PostItsIdentifier.get_identifier(self, parsed_args)

        headers = ['deleted', 'messages']
        deleted = []
        messages = []
        try:
            self.requests_client.delete(identifier)
            deleted.append(self.requests_client.build_url(identifier))
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]
        return (tuple(headers), tuple(data))
