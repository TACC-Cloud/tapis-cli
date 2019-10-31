from dotenv import set_key
from tapis_cli.mocks import FormatOne
from tapis_cli import settings
from .mixins import SettingName

__all__ = ['SettingsSet']


class SettingsSet(FormatOne, SettingName):
    """Set a Tapis CLI setting
    """
    def get_parser(self, prog_name):
        parser = super(SettingsSet, self).get_parser(prog_name)
        parser = SettingName.extend_parser(self, parser)
        parser.add_argument('settings_value',
                            metavar='<value>',
                            help='New value for setting')
        return parser

    def take_action(self, parsed_args):
        super(SettingsSet, self).take_action(parsed_args)
        self.validate_identifier(parsed_args.identifier, allow_private=False)
        env_file = settings.config.find_config()
        setting_name = parsed_args.identifier
        # TODO - Add some degree of validation, perhaps comparing inferred types for old and new value
        setting_value = parsed_args.settings_value
        set_key(env_file, setting_name, setting_value)
        headers = [setting_name]
        records = [setting_value]
        return (tuple(headers), tuple(records))
