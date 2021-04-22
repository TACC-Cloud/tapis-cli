import getpass
from agavepy.agave import Agave, AgaveError
from tapis_cli.display import Verbosity
from tapis_cli.constants import PLATFORM

from . import API_NAME, SERVICE_VERSION
from .models import Token
from .formatters import TokenFormatOne
from cliff.show import ShowOne
from tapis_cli.clients.services.mixins import JsonVerbose
__all__ = ['AuthShow']


class AuthShow(JsonVerbose, ShowOne):
    """Show current Tapis authentication configuration
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def take_action(self, parsed_args):
        # Load what we can from credentials cache.
        try:
            ag_context = Agave._read_current(agave_kwargs=True)
        except FileNotFoundError:
            # A very common case (all new tapis_cli installs, for instance), will
            # find NO cache file on disk. This must be recoverable, so set the
            # context to an empty dict
            raise FileNotFoundError(
                'Auth configuration was not loaded. Try running "tapis auth init".'
            )

        # Formulate a table view of key values for current session
        headers = [
            'tenant_id', 'username', 'api_key', 'access_token', 'expires_at',
            'refresh_token'
        ]
        data = [
        # Coerce to string to avoid failures where a deepcopy
        # operation in Python's implementation of tuple() is
        # unable to accomodate copying properties of an Agave object
            ag_context['tenant_id'],
            ag_context['username'],
            ag_context['api_key'],
            ag_context['token'],
            ag_context['expires_at'],
            ag_context['refresh_token']
        ]

        return (tuple(headers), tuple(data))
