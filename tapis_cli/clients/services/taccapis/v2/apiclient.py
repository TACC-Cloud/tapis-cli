import copy
import datetime
import json
import os
from agavepy.agave import Agave, AgaveError
from dateutil.tz import gettz
from tapis_cli.utils import datetime_to_isodate, datetime_to_human
from .direct import TaccApiDirectClient
import logging


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

    # Configures date rendering when the service returns datetime
    # results from a different timezone. Value is short name for a
    # timezone. See https://www.epochconverter.com/timezones
    TIMEZONE = None

    post_payload = {}

    def _get_direct(self, agave_client):
        return TaccApiDirectClient(agave_client)

    def init_clients(self, passed_args=None):
        self.tapis_client = Agave.restore()
        self.tapis_client.refresh()
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
            # Replace timezone in returned date
            # This works around a current bug in Aloe -
            # may need to revisit the implementation later
            if self.TIMEZONE is not None and isinstance(self.TIMEZONE, str):
                replacement_tz = gettz(self.TIMEZONE)
                value_orig = value
                value = value.replace(tzinfo=replacement_tz)
            if self.formatter_default == 'table':
                # TODO - figure out why this only works for the ShowOne
                value = datetime_to_human(value)
            else:
                value = datetime_to_isodate(value)
        return value

    def key_values(self):
        """Returns Tapis variable/value pairs for templating
        """
        api = dict()
        # Client data
        for k in ['api_server', 'tenant_id', 'api_key']:
            api[k] = getattr(self.tapis_client, k, None)

        # Profiles data
        profile_vars = ['email', 'username', 'first_name', 'last_name']

        try:
            try:
                profile = self.tapis_client.profiles.list(
                    username=api['username'])[0]
            except Exception:
                profile = self.tapis_client.profiles.get()

            for k in profile_vars:
                api[k] = profile.get(k, None)
            api['full_name'] = '{0} {1}'.format(api['first_name'],
                                                api['last_name'])

        except Exception:
            logging.warning(
                'Failed to resolve variables {0}. This is usually a side effect of impersonation under Tapis v2.'
                .format(profile_vars))

        # Implement legacy 'agave' template variables
        api['agave'] = copy.copy(api)

        # Default storage and execution systems
        api['default_public_storage'] = None
        api['default_public_execution'] = None
        api['default_private_storage'] = None
        api['default_private_execution'] = None
        try:
            default_systems = self.tapis_client.systems.list(default=True)
            for s in default_systems:
                s_type = s.get('type', False)
                s_public = s.get('public', False)
                s_id = s.get('id')
                if s_type == 'STORAGE':
                    if s_public:
                        api['default_public_storage'] = s_id
                    else:
                        api['default_private_storage'] = s_id
                elif s_type == 'EXECUTION':
                    if s_public:
                        api['default_public_execution'] = s_id
                    else:
                        api['default_private_execution'] = s_id
        except Exception:
            pass

        return api
