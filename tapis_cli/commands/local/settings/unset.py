from dotenv import unset_key
from tapis_cli.mocks import FormatOne
from tapis_cli import settings
from .mixins import SettingName

__all__ = ['SettingsUnset']


class SettingsUnset(FormatOne, SettingName):
    """Unset a Tapis CLI setting
    """
    def get_parser(self, prog_name):
        parser = super(SettingsUnset, self).get_parser(prog_name)
        parser = SettingName.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        super(SettingsUnset, self).take_action(parsed_args)
        self.validate_identifier(parsed_args.identifier, allow_private=False)
        env_file = settings.config.find_config()
        setting_name = parsed_args.identifier
        unset_key(env_file, setting_name)
        headers = [setting_name]
        records = [
            'Run "tapis settings get {0}" to see current value'.format(
                setting_name)
        ]
        return (tuple(headers), tuple(records))
