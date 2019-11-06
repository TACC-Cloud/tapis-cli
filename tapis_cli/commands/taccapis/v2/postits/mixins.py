from tapis_cli.clients.services.mixins import ServiceIdentifier, InvalidValue

__all__ = ['PostItsIdentifier']


class PostItsIdentifier(ServiceIdentifier):
    """Configures a Command to require a mandatory Post-it
    """
    service_id_type = 'PostIt'
    dest = 'postit_id'

    def validate_identifier(self, identifier, permissive=False):
        if len(identifier) == 32:
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidValue(
                    '{0} not a valid Post-it Identifier'.format(identifier))
