import json
import os
from agavepy.agave import Agave
from .request import Swaggerless


class TaccApiClient(object):
    # Agave kwarg => ~/.agave/current key name => command.property
    PROPS = [('token', 'access_token', 'access_token'),
             ('refresh_token', 'refresh_token', 'refresh_token'),
             ('api_key', 'api_key', 'api_key'),
             ('api_secret', 'api_secret', 'api_secret'),
             ('api_server', 'baseurl', 'api_server'),
             ('tenant_id', 'tenantid', 'tenant_id'),
             ('username', 'username', 'username'),
             ('created_at', 'created_at', 'created_at'),
             ('expires_in', 'expires_in', 'expires_in'),
             ('expires_at', 'expires_at', 'expires_at')]

    def init_clients(self, parsed_args=dict()):
        # To pick up client properties set using parameters set up from
        # inherited parsers, this must be called at the end of the
        # inheritance chain, immediately before getting to work
        # making API calls

        # 1. Read from local JSON cache
        # 2. Process overrides from parser args
        # 3. Init the client(s)
        current = json.load(open(os.path.expanduser('~/.agave/current'), 'r'))
        # raise SystemError(current)
        config = dict()
        for e, k, p in self.PROPS:
            parsed_arg = getattr(parsed_args, p, None)
            current_arg = current.get(k, None)
            if parsed_arg is not None:
                config[e] = parsed_arg
            elif current_arg is not None:
                config[e] = current_arg

        ag = Agave(**config)
        self.tapis_client = ag
        #        self.tapis_client = Agave.restore()
        # for requests made directly via requests module
        self.requests_client = Swaggerless(self.tapis_client)
