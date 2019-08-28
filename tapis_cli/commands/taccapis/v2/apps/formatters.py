import datetime

from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany)
from tapis_cli.utils import datetime_to_isodate, datetime_to_human
from .models import App


class AppsBase(TaccApisBase):
    id_display_name = App.id_display_name
    post_payload = dict()

    def take_action_defaults(self, parsed_args):
        return self

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        return ((), ())

    def render_value(self, value):
        if isinstance(value, datetime.datetime):
            if self.formatter_default == 'table':
                # TODO - figure out why this only works for the ShowOne
                value = datetime_to_human(value)
            else:
                value = datetime_to_isodate(value)
        return value


class AppsFormatOne(TaccApisFormatOne, AppsBase):
    def take_action_defaults(self, parsed_args):
        super().take_action_defaults(parsed_args)
        return self


class AppsFormatMany(TaccApisFormatMany, AppsBase):
    def take_action_defaults(self, parsed_args):
        super().take_action_defaults(parsed_args)
        self.post_payload['limit'] = parsed_args.limit
        self.post_payload['offset'] = parsed_args.offset
        return self
