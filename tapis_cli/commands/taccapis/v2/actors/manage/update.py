from ..mixins import ActorIdentifier
from ..models import Actor
from .base import ActorsBaseClass

__all__ = ['ActorsUpdate']


class ActorsUpdate(ActorsBaseClass):
    CREATE_ONLY = False
    HELP_STRING = 'Update an Actor'
    LEGACY_COMMMAND_STRING = 'abaco update'

    def take_action(self, parsed_args):
        super().take_action(parsed_args)

        headers = self.render_headers(Actor, parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        rec = self.tapis_client.actors.update(actorId=actor_id,
                                              body=self.config)

        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
