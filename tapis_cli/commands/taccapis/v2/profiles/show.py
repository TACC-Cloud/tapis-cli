from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.taccapis.v2.bearer import TapisServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import Profile
from .formatters import ProfilesFormatOne

__all__ = ['ProfilesShow']


class ProfilesShow(TapisServiceIdentifier, ProfilesFormatOne):
    """Show a single user profile
    """
    VERBOSITY = Verbosity.RECORD

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = Profile().get_headers(self.VERBOSITY, parsed_args.formatter)

        rec = self.tapis_client.profiles.listByUsername(
            username=parsed_args.identifier)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
