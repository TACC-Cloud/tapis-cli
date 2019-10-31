from tapis_cli.mocks import FormatOne
from tapis_cli import settings
from .mixins import SettingName

__all__ = ['SettingsGet']


class SettingsGet(FormatOne, SettingName):
    """Get a Tapis CLI setting
    """
    def get_parser(self, prog_name):
        parser = super(SettingsGet, self).get_parser(prog_name)
        parser = SettingName.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        super(SettingsGet, self).take_action(parsed_args)
        self.validate_identifier(parsed_args.identifier, allow_private=True)
        headers = []
        records = []
        for s, v in settings.all_settings().items():
            if s == parsed_args.identifier.upper():
                headers.append(s)
                records.append(v)
        return (tuple(headers), tuple(records))
