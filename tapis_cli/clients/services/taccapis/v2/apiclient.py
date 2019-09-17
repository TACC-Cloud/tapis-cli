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

    def init_clients(self, parsed_args=dict()):
        # To pick up client properties set using parameters set up from
        # inherited parsers, this must be called at the end of the
        # inheritance chain, immediately before getting to work
        # making API calls

        # 1. Read from local JSON cache
        # 2. Process overrides from parser args
        # 3. Init the client(s)
        # TODO - use Agavepy public API for getting this
        # current = json.load(open(os.path.expanduser('~/.agave/current'), 'r'))
        # config = dict()
        # for e, k, p in self.PROPS:
        #     parsed_arg = getattr(parsed_args, p, None)
        #     current_arg = current.get(k, None)
        #     if parsed_arg is not None:
        #         config[e] = parsed_arg
        #     elif current_arg is not None:
        #         config[e] = current_arg

        # ag = Agave(**config)
        # self.tapis_client = ag
        # self.tapis_client.token.refresh()
        #        self.tapis_client = Agave.restore()
        # for requests made directly via requests module
        # TODO - only populate this if there is an access_token
        # TODO - Come back and re-enable overrides via CLI option
        self.tapis_client = Agave.restore()
        self.requests_client = TaccApiDirectClient(self.tapis_client)
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
