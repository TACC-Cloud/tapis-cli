from tapis_cli.clients.services.mixins import ServiceIdentifier

__all__ = ['ActorIdentifier']


class ActorIdentifier(ServiceIdentifier):
    service_id_type = 'Actor'
    dest = 'actor_id'
