from ..models import Actor
from .base import ActorsBaseClass

__all__ = ['ActorsCreate']


class ActorsCreate(ActorsBaseClass):
    CREATE_ONLY = True
    HELP_STRING = 'Create an Actor'
    LEGACY_COMMMAND_STRING = 'abaco create'

    def take_action(self, parsed_args):
        super().take_action(parsed_args)

        headers = self.render_headers(Actor, parsed_args)
        rec = self.tapis_client.actors.add(body=self.config)

        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
