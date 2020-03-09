from configparser import SectionProxy
from tapis_cli.commands.taccapis.formatters import (
    TaccApisFormatManyUnlimited, TaccApisFormatOne)
from tapis_cli.clients.services.mixins import UploadJSONTemplate
from tapis_cli.templating import dot_notation
from tapis_cli.project_ini import generate_template_ini, save_config

__all__ = ['VariablesList', 'VariablesInit']


class VariablesList(TaccApisFormatManyUnlimited, UploadJSONTemplate):
    HELP_STRING = 'Show active template variable names and values'

    def get_parser(self, prog_name):
        parser = super(VariablesList, self).get_parser(prog_name)
        parser = UploadJSONTemplate.extend_parser(self, parser)
        parser.add_argument('-A',
                            '--all',
                            dest='show_all',
                            action='store_false',
                            help='Also show empty variables')
        return parser

    def take_action(self, parsed_args):
        self.init_clients(parsed_args)
        tackv = self.all_key_values(parsed_args, None)
        flat_vars = {}
        for k, v in tackv.items():
            # grants is a special section
            if k != 'grants':
                # print(k, type(v))
                if not isinstance(v, (SectionProxy, dict)):
                    flat_vars[k] = v
                else:
                    dotted_vars = dot_notation({k: v})
                    for k1, v1 in dotted_vars.items():
                        flat_vars[k1] = v1

        # Filter empty values
        if parsed_args.show_all:
            flat_vars = {
                k: v
                for (k, v) in flat_vars.items()
                if (v is not None) and (v != '')
            }

        flat_vars = sorted(flat_vars.items())
        # records = []
        # for k, v in tackv.items():
        #     records.append([k, v])
        headers = ['variable', 'current_value']
        return (tuple(headers), tuple(flat_vars))


class VariablesInit(TaccApisFormatOne):

    HELP_STRING = 'Create an .ini file to support templating'

    # tapis info vars init <filename>
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser.add_argument(
            'ini_file_name',
            metavar='FILENAME',
            nargs='?',
            default='project.ini',
            help=
            'Optional ini filename (must be one of: project.ini, app.ini. actor.ini)'
        )
        return parser

    def take_action(self, parsed_args):
        ini_doc = generate_template_ini()
        created = []
        exceptions = []

        try:
            save_config(ini_doc, parsed_args.ini_file_name)
            created.append(parsed_args.ini_file_name)
        except Exception as e:
            exceptions.append(e)

        headers = ['created', 'messages']
        data = [created, [str(e) for e in exceptions]]

        return (tuple(headers), tuple(data))
