from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import MetadataFormatOne
from .mixins import MetadataUUID

__all__ = ['MetadataPemsShow']


class MetadataPemsShow(MetadataFormatOne, MetadataUUID, Username):

    HELP_STRING = 'Show Permissions on a Metadata document for specific User'
    LEGACY_COMMMAND_STRING = 'metadata-pems-list'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(MetadataPemsShow, self).get_parser(prog_name)
        parser = MetadataUUID.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = MetadataUUID.get_identifier(self, parsed_args)
        self.update_payload(parsed_args)

        headers = self.render_headers(Permission, parsed_args)
        rec = self.tapis_client.meta.listMetadataPermissionsForUser(
            uuid=identifier, username=parsed_args.username)

        # TODO - Account for the wierd behavior where querying ANY username
        # will return +rwx even if the username is fictitious. A client-side
        # (partial) would be to list the pems, extract the usernames, and
        # validate presence of <username> among the. Another would be to
        # simply list all pems and extract the matching row by <username>

        record = []
        if self.app_verbose_level > self.VERBOSITY:
            # Table display
            record.append(rec.get('username'))
            record.extend(Permission.pem_to_row(rec.get('permission', {})))
        else:
            # Verbose JSON display
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)

        return (headers, record)
