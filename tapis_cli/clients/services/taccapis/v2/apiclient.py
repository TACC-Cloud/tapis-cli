import datetime
import json
import os
from agavepy.agave import Agave
from tapis_cli.utils import datetime_to_isodate, datetime_to_human
from .direct import TaccApiDirectClient


class TaccApiClient(object):
    # (Agave.__init__ kwarg, ~/.agave/current key, parsed_arg.attr)
    PROPS = [('token', 'access_token', 'access_token'),
             ('refresh_token', 'refresh_token', 'refresh_token'),
             ('api_key', 'api_key', 'api_key'),
             ('api_secret', 'api_secret', 'api_secret'),
             ('api_server', 'baseurl', 'api_server'),
             ('tenant_id', 'tenantid', 'tenant_id'),
             ('username', 'username', 'username'),
             ('token_username', 'token_username', 'token_username'),
             ('password', 'password', 'password'),
             ('created_at', 'created_at', 'created_at'),
             ('expires_in', 'expires_in', 'expires_in'),
             ('expires_at', 'expires_at', 'expires_at')]

    post_payload = dict()

    def _get_direct(self, agave_client):
        return TaccApiDirectClient(agave_client)

    def init_clients(self, passed_args=None):
        self.tapis_client = Agave.restore()
        self.tapis_client.token.refresh()
        self.requests_client = self._get_direct(self.tapis_client)
        return self

    def render_value(self, value):
        """Renders a value based on current display format

        Each field value in a response can be passed through this function
        to implement format-specific rendering
        """
        # If the value is a date/time and display is a table, render as
        # a human-readable value instead of an ISO-8601 date
        if isinstance(value, datetime.datetime):
            if self.formatter_default == 'table':
                # TODO - figure out why this only works for the ShowOne
                value = datetime_to_human(value)
            else:
                value = datetime_to_isodate(value)
        return value
