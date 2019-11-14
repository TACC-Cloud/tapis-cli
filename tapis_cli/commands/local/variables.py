from configparser import SectionProxy
from tapis_cli.commands.taccapis.formatters import TaccApisFormatManyUnlimited
from tapis_cli.clients.services.mixins import UploadJSONTemplate
from tapis_cli.templating import dot_notation

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
        flat_vars = {}
        for k, v in tackv.items():
            print(k, type(v))
            if not isinstance(v, SectionProxy):
                flat_vars[k] = v
            else:
                dotted_vars = dot_notation({k: v})
                for k1, v1 in dotted_vars.items():
                    flat_vars[k1] = v1

        flat_vars = sorted(flat_vars.items())
        # records = []
        # for k, v in tackv.items():
        #     records.append([k, v])
        headers = ['variable', 'current_value']
        return (tuple(headers), tuple(flat_vars))
