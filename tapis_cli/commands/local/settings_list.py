from tapis_cli.mocks import FormatMany
from tapis_cli import settings


class SettingsList(FormatMany):
    """List current Tapis CLI settings
    """
    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = ['Setting', 'Value']
        records = []
        for s, v in settings.all_settings().items():
            records.append([s, v])
        return (tuple(headers), tuple(records))
