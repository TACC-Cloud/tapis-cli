import datetime

from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany)
from tapis_cli.utils import datetime_to_isodate, datetime_to_human
from .models import Profile

__all__ = ['ProfilesFormatOne', 'ProfilesFormatMany']


class ProfilesBase(TaccApisBase):
    id_display_name = Profile.id_display_name
    post_payload = dict()

    def take_action_defaults(self, parsed_args):
        return self

    def render_value(self, value):
        if isinstance(value, datetime.datetime):
            if self.formatter_default == 'table':
                # TODO - figure out why this only works for the ShowOne
                value = datetime_to_human(value)
            else:
                value = datetime_to_isodate(value)
        return value


class ProfilesFormatOne(TaccApisFormatOne, ProfilesBase):
    pass


class ProfilesFormatMany(TaccApisFormatMany, ProfilesBase):
    pass
