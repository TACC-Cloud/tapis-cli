from tapis_cli.clients.services.mixins import InvalidValue, TapisEntityUUID

__all__ = ['JobsUUID']


class JobsUUID(TapisEntityUUID):
    """Configures a Command to require a mandatory Tapis job UUID
    """
    service_id_type = 'Job'
    dest = 'job_uuid'

    def validate_identifier(self, identifier, permissive=False):
        if len(identifier) >= 36 and len(
                identifier) <= 40 and identifier.endswith('-007'):
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidValue(
                    '{0} not a valid Job UUID'.format(identifier))
