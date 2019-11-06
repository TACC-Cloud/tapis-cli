from tapis_cli.clients.services.mixins import ServiceIdentifier

__all__ = ['AppIdentifier']


class AppIdentifier(ServiceIdentifier):
    service_id_type = 'App'
    dest = 'app_id'
