"""Settings-specfic mixins
"""

from tapis_cli.clients.services.mixins import (ServiceIdentifier,
                                               InvalidIdentifier)
from tapis_cli.settings import all_settings

__all__ = ['SettingName']


class UnknownSetting(InvalidIdentifier):
    pass


class SettingName(ServiceIdentifier):
    @classmethod
    def arg_display(cls, id_value):
        return 'SETTING_NAME'

    @classmethod
    def arg_metavar(cls, id_value):
        return cls.arg_display(id_value)

    @classmethod
    def arg_help(cls, id_value):
        return 'Tapis setting name'

    def validate_identifier(self,
                            identifier,
                            allow_private=False,
                            permissive=False):
        if identifier.startswith('_') and allow_private is not True:
            raise ValueError('{0} is a private setting'.format(identifier))
        if identifier in list(all_settings().keys()):
            return True
        else:
            if permissive:
                return False
            else:
                raise UnknownSetting(
                    '{0} not a known setting'.format(identifier))
