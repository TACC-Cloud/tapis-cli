from tapis_cli.commands.taccapis.formatters import TaccApisFormatManyUnlimited
from tapis_cli.clients.services.mixins import UploadJSONTemplate

__all__ = ['VariablesList']

class VariablesList(TaccApisFormatManyUnlimited, UploadJSONTemplate):
    """Show current template variable names and values
    """

    def get_parser(self, prog_name):
        parser = super(VariablesList, self).get_parser(prog_name)
        parser = UploadJSONTemplate.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        self.init_clients(parsed_args)
        tackv = self.all_key_values(parsed_args, None)
        tackv = sorted(tackv.items())
        # records = []
        # for k, v in tackv.items():
        #     records.append([k, v])
        headers = ['variable', 'current_value']
        return (tuple(headers), tuple(tackv))
