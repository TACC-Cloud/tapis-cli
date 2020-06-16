from tapis_cli.clients.services.mixins import ServiceIdentifier

__all__ = ['AppIdentifier']


class AppIdentifier(ServiceIdentifier):
    service_id_type = 'App'
    dest = 'app_id'

    def validate_identifier(self, identifier, permissive=False):
        try:
            self.tapis_client.apps.get(appId=identifier)
            return True
        except Exception:
            if permissive:
                return False
            else:
                raise ValueError(
                    'No application exists with ID {}'.format(identifier))
