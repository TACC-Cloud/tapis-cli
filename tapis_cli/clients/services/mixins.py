"""Mix-ins used to add defined behaviors to Tapis CLI commands
"""
import argparse
import copy
import json
import os
import sys
import validators
import docker as dockerpy

from agavepy.agave import Agave, AgaveError

from cliff.command import Command
from cliff.hooks import CommandHook
from cliff.app import App

from tapis_cli import constants, settings
from tapis_cli.display import Verbosity
from tapis_cli.utils import serializable
from tapis_cli import project_ini, settings, templating

__all__ = [
    'OptionNotImplemented', 'AppVerboseLevel', 'JsonVerbose',
    'ServiceIdentifier', 'UploadJsonFile', 'AgaveURI', 'RemoteFilePath',
    'LocalFilePath', 'Username', 'InvalidIdentifier', 'OptionalLocalFilePath',
    'InvalidValue', 'URL', 'TapisEntityUUID', 'OptionalTapisEntityUUID',
    'UploadJSONTemplate', 'WorkingDirectory', 'WorkingDirectoryOpt',
    'WorkingDirectoryArg', 'DownloadDirectoryArg', 'DockerPy',
    'LegacyCommmandHelp', 'FilesURI', 'IniLoader'
]


class InvalidValue(ValueError):
    pass


class InvalidIdentifier(InvalidValue):
    """Raised when an invalid identifier is encountered
    """
    pass


class OptionNotImplemented(ValueError):
    """Raised when an option that is only a placeholder is specified
    """
    pass


class LegacyCommmandHelp(object):
    """Configures a commands to show legacy syntax

    Bash CLI syntax is shown in overview and detailed help responses.
    This is configurable at class level with SHOW_LEGACY_INTERACTIVE and 
    RENDER_LEGACY_DOCS booleans. It is also configurable for overview mode 
    via settings.TAPIS_CLI_SHOW_LEGACY_INTERACTIVE_HELP.
    """

    SHOW_LEGACY_INTERACTIVE = False
    RENDER_LEGACY_DOCS = True

    HELP_STRING = 'Command description'
    # Keep short in case the string is displayed in overview mode
    LEGACY_COMMMAND_STRING = None

    @property
    def _description(self):
        resp = self.HELP_STRING
        if self.LEGACY_COMMMAND_STRING is not None and (
                self.SHOW_LEGACY_INTERACTIVE
                and settings.TAPIS_CLI_SHOW_LEGACY_INTERACTIVE_HELP):
            resp = resp + ' ({0})'.format(self.LEGACY_COMMMAND_STRING)
        return resp

    def get_epilog(self):
        if self.LEGACY_COMMMAND_STRING is not None and self.RENDER_LEGACY_DOCS:
            return 'Replaces legacy CLI command "{0}"\n'.format(
                self.LEGACY_COMMMAND_STRING)
        else:
            return '\n'


class ParserExtender(object):

    working_dir = '.'

    def getwd(self):
        return getattr(self, 'working_dir')

    def extend_parser(self, parser):
        # When sublcassing: DO NOT FORGET TO RETURN PARSER
        return parser

    def preprocess_args(self, parsed_args):
        # When sublcassing: DO NOT FORGET TO RETURN PARSED_ARGS
        return parsed_args

    def render_extended_parser_value(self, key, value, formatter=None):
        return key, value

    def validate(self, value, permissive=True):
        """Placeholder to implement validation of a value passed
        via a ParserExtender
        """
        if value is not None:
            return True
        else:
            return False


class AppVerboseLevel(ParserExtender):
    """Configures a Command to access the parent cliff App's verbosity level

    The calling App's verbose_level is made available via method
    app_verbose_level(). In addition, two properties 'VERBOSITY' and
    'EXTRA_VERBOSITY' are defined. These are intended to be values defined
    by the `Verbosity` module. 'VERBOSITY' is the default field-display
    verbosity for the Command, while `EXTRA_VERBOSITY` is the verbosity level
    when a user or process specifies that additional verbosity is needed.
    """
    VERBOSITY = None
    EXTRA_VERBOSITY = VERBOSITY

    @property
    def app_verbose_level(self):
        """Exposes the app-scoped verbosity level as a formatter property
        """
        vlevel = 1
        try:
            vlevel = self.app_args.verbose_level
        except Exception:
            pass
        return vlevel


class JsonVerbose(AppVerboseLevel):
    """Configures a Command to use JSON as formatter when verbose is requested

    Overrides the Command.formatter_default property such that passing an
    instance of '-v' to the cliff App when running a command will configure the
    Command to use JSON formatter and to increase its field-display verbosity
    to the level defined by 'EXTRA_VERBOSITY'
    """
    EXTRA_VERBOSITY = Verbosity.RECORD

    @property
    def formatter_default(self):
        """Overrides formatter_default to return JSON when -v is passed
        """
        if self.app_verbose_level > 1:
            return 'json'
        else:
            return 'table'

    def verbosify_parsed_args(self, parsed_args):
        if self.app_verbose_level > 1:
            # raise SystemError(dir(self.app.options))
            parsed_args.formatter = 'json'
            if self.EXTRA_VERBOSITY is not None:
                self.VERBOSITY = self.EXTRA_VERBOSITY
        return parsed_args

    def preprocess_args(self, parsed_args):
        parsed_args = super(JsonVerbose, self).preprocess_args(parsed_args)
        if self.app_verbose_level > 1:
            parsed_args.formatter = 'json'
            if self.EXTRA_VERBOSITY is not None:
                self.VERBOSITY = self.EXTRA_VERBOSITY
        return parsed_args


class ServiceIdentifier(ParserExtender):
    """Configures a Command to require a mandatory 'identifier' positional param

    Adds a positional parameter to the Command parser. The value for the
    parameter's 'metavar' is set by the Command.service_id_type property.
    """
    # Stem for naming the identifier
    service_id_type = 'Service'
    # Leaf for naming the identifier
    id_type = 'identifier'
    # If True, the argument is optional
    optional = False
    # argparse destination
    dest = id_type

    # @classmethod
    def arg_display(self, id_value):
        return '{0}_id'.format(id_value).lower()

    # @classmethod
    def arg_metavar(self, id_value):
        return self.arg_display(id_value)

    # @classmethod
    def arg_help(self, id_value):
        if not self.optional:
            return '{0} {1}'.format(id_value, self.id_type)
        else:
            return 'Optional {0} {1}'.format(id_value, self.id_type)

    def extend_parser(self, parser):
        id_value = getattr(self, 'service_id_type')
        if id_value is not None:
            arg_display = '{0}_id'.format(id_value).lower()
        if self.optional:
            nargs = '?'
        else:
            nargs = None
        if id_value is not None:
            parser.add_argument(self.dest,
                                type=str,
                                nargs=nargs,
                                metavar=self.arg_metavar(id_value).upper(),
                                help=self.arg_help(id_value))
        return parser

    def validate_identifier(self, identifier, permissive=True):
        return True

    def get_identifier(self, parsed_args, validate=False, permissive=False):
        identifier = None
        try:
            identifier = getattr(parsed_args, self.dest)
            # identifier = parsed_args.identifier
            self.validate_identifier(identifier)
        except Exception:
            if permissive:
                return None
            else:
                raise
        return identifier


class TapisEntityUUID(ServiceIdentifier):
    service_id_type = 'Tapis Entity'
    id_type = 'unique identifer'

    @classmethod
    def arg_display(cls, id_value):
        return '{0}_uuid'.format(id_value).lower()


class OptionalTapisEntityUUID(TapisEntityUUID):
    optional = True


class RemoteFilePath(ParserExtender):
    """Configures a Command to accept an optional file path
    """
    def extend_parser(self, parser):
        parser.add_argument('file_path',
                            default='.',
                            nargs='?',
                            metavar='FILEPATH',
                            help='File path relative to output directory')
        return parser


class LocalFilePath(ParserExtender):
    """Configures a Command to accept a local file path
    """
    def extend_parser(self, parser):
        parser.add_argument('local_file_path',
                            metavar='FILEPATH',
                            help='Path (relative to working directory)')
        return parser


class OptionalLocalFilePath(ParserExtender):
    """Configures a Command to accept a local file path
    """
    def extend_parser(self, parser):
        parser.add_argument(
            'local_file_path',
            nargs='?',
            metavar='FILEPATH',
            help='Optional path (relative to working directory)')
        return parser


class WorkingDirectory(ParserExtender):
    """Allows the working directory to be set via positional argument.
    """
    help_string = 'Working directory'

    def extend_parser(self, parser):
        parser.add_argument('working_directory',
                            metavar='DIRECTORY',
                            default='.',
                            type=str,
                            help=self.help_string)
        return parser

    def set_working_directory(self, parsed_args, working_dir='.'):
        wd_value = getattr(parsed_args, 'working_directory', working_dir)
        setattr(self, 'working_dir', wd_value)
        return self


class WorkingDirectoryOpt(WorkingDirectory):
    """Allows the working directory to be set via optional, terminal argument.
    """
    def extend_parser(self, parser):
        parser.add_argument('working_directory',
                            metavar='DIRECTORY',
                            default='.',
                            nargs='?',
                            type=str,
                            help=self.help_string)
        return parser


class WorkingDirectoryArg(WorkingDirectory):
    """Allows the working directory to be set via optional argument.
    """
    def extend_parser(self, parser):
        parser.add_argument('-W',
                            dest='working_directory',
                            metavar='DIRECTORY',
                            default='.',
                            type=str,
                            help=self.help_string)
        return parser


class DownloadDirectoryArg(WorkingDirectoryArg):
    """Allows the working directory to be set via optional argument.
    """
    help_string = 'Download directory'

    def extend_parser(self, parser):
        parser.add_argument('-W',
                            dest='working_directory',
                            metavar='DIRECTORY',
                            default='.',
                            type=str,
                            help=self.help_string)
        return parser


class UploadJsonFile(ParserExtender):
    """Configures a client to accept and load a JSON file

    Adds -F and --file to a Command's parser. To load the designated file,
    the handle_file_upload() must then be called. JSON file contents will
    reside in self.json_file_contents.
    """
    json_loaded = dict()
    validate = True
    optional = False
    default = None

    def extend_parser(self, parser):
        if self.default is None:
            parser.add_argument('-F',
                                '--file',
                                dest='json_file_name',
                                metavar='FILEPATH',
                                type=str,
                                help='JSON payload file')
        else:
            parser.add_argument('-F',
                                '--file',
                                dest='json_file_name',
                                metavar='FILEPATH',
                                default=self.default,
                                type=str,
                                help='JSON payload file ({})'.format(
                                    self.default))
        return parser

    def handle_file_upload(self, parsed_args):
        document_path, document_source = None, None
        if parsed_args.json_file_name == '-':
            document_source = sys.stdin
        elif parsed_args.json_file_name is None:
            if self.optional:
                setattr(self, 'json_file_contents', {})
                return self.json_file_contents
            else:
                raise ValueError('JSON file path must be specified')
        else:
            document_path = os.path.join(self.getwd(),
                                         parsed_args.json_file_name)

        document_source = open(document_path, 'rb')

        # Load up the data source, validating that it's minimally serializable
        # TODO - factor validation into its own method so it can be overridden
        try:
            payload = json.load(document_source)
            if self.validate:
                serializable(payload)
            setattr(self, 'json_file_contents', payload)
            return self.json_file_contents
        except Exception as exc:
            setattr(self, 'json_file_contents', None)
            raise ValueError('{0} was not valid JSON: {1}'.format(
                parsed_args.json_file_name, exc))


class IniLoader(ParserExtender):
    def extend_parser(self, parser):
        parser = super(IniLoader, self).extend_parser(parser)
        parser.add_argument('--ini',
                            dest='ini_file_name',
                            metavar='FILEPATH',
                            type=str,
                            help='.ini file (project.ini)')
        return parser

    def get_ini_path(self, filename):
        return project_ini.config_path(filename, self.getwd())

    def get_ini_contents(self, parsed_args):
        ini_path = self.get_ini_path(parsed_args.ini_file_name)
        p = project_ini.key_values(ini_path)
        return p


class UploadJSONTemplate(IniLoader, UploadJsonFile):
    #class UploadJSONTemplate(UploadJsonFile):
    # def extend_parser(self, parser):
    #     parser = super(UploadJSONTemplate, self).extend_parser(parser)
    #     parser.add_argument('--ini',
    #                         dest='ini_file_name',
    #                         metavar='FILEPATH',
    #                         type=str,
    #                         help='.ini file (project.ini)')
    #     return parser

    # def get_ini_path(self, filename):
    #     return project_ini.config_path(filename, self.getwd())

    # OVERRIDES DO NOT SEEM TO BE WORKING
    def _all_key_values(self, parsed_args, passed_vals):
        t = templating.key_values(passed_vals)
        ini_path = self.get_ini_path(parsed_args.ini_file_name)
        p = project_ini.key_values(ini_path)
        project_ini.update_config(t, p, add_keys=True)

        # tapis dynamic variables
        tapis = self.key_values()
        # right-merge dictionary
        # dynamic values always overide ini-loaded defaults
        project_ini.update_config(t, tapis, add_keys=True)

        # Compute default execution and deployment systems
        defaults = {
            'app': {
                'execution_system': None,
                'deployment_system': None
            }
        }
        if settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM is not None and settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM != '':
            defaults['app'][
                'execution_system'] = settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM
        else:
            defaults['app']['execution_system'] = tapis.get(
                'default_private_execution',
                tapis.get('default_public_execution', None))
        if settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM is not None and settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM != '':
            defaults['app'][
                'deployment_system'] = settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM
        else:
            defaults['app']['deployment_system'] = tapis.get(
                'default_private_storage',
                tapis.get('default_public_storage', None))

        # right-merge dictionary
        project_ini.update_config(t, defaults, add_keys=True)
        return t

    # OVERRIDES DO NOT SEEM TO BE WORKING
    def all_key_values(self, parsed_args, passed_vals):
        # Load up ini file
        ini_path = self.get_ini_path(parsed_args.ini_file_name)
        cfg = project_ini.key_values(ini_path)

        # Load up core template vars
        tmpl = templating.key_values({})

        project_ini.update_config(cfg, tmpl, add_keys=True)

        # Extend with API-related dynamic vars
        tapis = self.key_values()
        project_ini.update_config(cfg, tapis, add_keys=True)

        # Compute and merge in default execution and deployment systems
        # consult settings first, then resolve from tapis config if defaults arent learnable
        defaults = {
            'app': {
                'execution_system': None,
                'deployment_system': None
            }
        }
        if settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM is not None and settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM != '':
            defaults['app'][
                'execution_system'] = settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM
        else:
            if tapis.get('default_private_execution', None) is not None:
                defaults['app']['execution_system'] = tapis.get(
                    'default_private_execution')
            elif tapis.get('default_public_execution', None) is not None:
                defaults['app']['execution_system'] = tapis.get(
                    'default_public_execution')
            else:
                defaults['app']['execution_system'] = None

        if settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM is not None and settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM != '':
            defaults['app'][
                'deployment_system'] = settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM
        else:
            if tapis.get('default_private_storage', None) is not None:
                defaults['app']['deployment_system'] = tapis.get(
                    'default_private_storage')
            elif tapis.get('default_public_storage', None) is not None:
                defaults['app']['deployment_system'] = tapis.get(
                    'default_public_storage')
            else:
                defaults['app']['deployment_system'] = None

        # right-merge dictionary
        project_ini.update_config(cfg, defaults, add_keys=True)

        # Finally, layer over passed values. Assumption is that these
        # are passed by CLI or other run-time means
        project_ini.update_config(cfg, passed_vals, add_keys=True)
        return cfg

    def _render_json_file_contents(self, passed_vals):
        """Transform the JSON file contents by rendering it as a Jinja template
        """
        payload = getattr(self, 'json_file_contents')
        txt_payload = json.dumps(payload)
        txt_payload = templating.render_template(txt_payload,
                                                 passed_vals=passed_vals)
        payload = json.loads(txt_payload)
        setattr(self, 'json_file_contents', payload)
        return self.json_file_contents

    def handle_file_upload(self, parsed_args, passed_vals={}):
        super(UploadJSONTemplate, self).handle_file_upload(parsed_args)
        # payload = getattr(self, 'json_file_contents')
        # load variable sets
        # ini-based configuration
        ini_path = self.get_ini_path(parsed_args.ini_file_name)
        config = project_ini.key_values(ini_path, as_dict=True)
        # tapis dynamic variables
        tapis = self.key_values()
        # right-merged dictionary
        # dynamic values always overide ini-loaded defaults
        project_ini.update_config(config, tapis, add_keys=True)

        # Compute and merge in default execution and deployment systems
        # consult settings first, then resolve from tapis config if defaults arent learnable
        defaults = {
            'app': {
                'execution_system': None,
                'deployment_system': None
            }
        }
        if settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM is not None and settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM != '':
            defaults['app'][
                'execution_system'] = settings.TAPIS_CLI_PREF_EXECUTION_SYSTEM
        else:
            if tapis.get('default_private_execution', None) is not None:
                defaults['app']['execution_system'] = tapis.get(
                    'default_private_execution')
            elif tapis.get('default_public_execution', None) is not None:
                defaults['app']['execution_system'] = tapis.get(
                    'default_public_execution')
            else:
                defaults['app']['execution_system'] = None

        if settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM is not None and settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM != '':
            defaults['app'][
                'deployment_system'] = settings.TAPIS_CLI_PREF_DEPLOYMENT_SYSTEM
        else:
            if tapis.get('default_private_storage', None) is not None:
                defaults['app']['deployment_system'] = tapis.get(
                    'default_private_storage')
            elif tapis.get('default_public_storage', None) is not None:
                defaults['app']['deployment_system'] = tapis.get(
                    'default_public_storage')
            else:
                defaults['app']['deployment_system'] = None
        project_ini.update_config(config, defaults, add_keys=True)

        # Accept run-time overrides
        project_ini.update_config(config, passed_vals, add_keys=True)
        # render, where merged variables overrides module-provided values
        self._render_json_file_contents(passed_vals=config)
        return self.json_file_contents


class Username(ParserExtender):
    """Configures a Command to accept an positional username
    """
    def extend_parser(self, parser):
        parser.add_argument('username',
                            metavar='USERNAME',
                            help='{0} username'.format(constants.PLATFORM))
        return parser


class DockerPy:
    dockerpy = None

    def docker_client_from_env(self):
        setattr(self, 'dockerpy', dockerpy.from_env())


class URL(ParserExtender):
    """Configures a Command to require a mandatory 'url' positional parameter
    """
    def get_value(self, parsed_args):
        return parsed_args.uri

    def extend_parser(self, parser):
        parser.add_argument('url',
                            type=str,
                            metavar='URL',
                            help='Valid URL [http(s)://]')
        return parser

    def validate(self, url, permissive=False):
        try:
            validators.url(url, public=True)
            return True
        except Exception:
            if permissive:
                return False
            else:
                raise


class AgaveURI(ParserExtender):
    """Configures a Command to require a mandatory 'agave uri'
    positional parameter
    """
    def get_value(self, parsed_args):
        return parsed_args.agave_uri

    def extend_parser(self, parser):
        parser.add_argument('agave_uri',
                            type=str,
                            metavar='AGAVE_URI',
                            help='Files URI (agave://)')
        return parser

    @classmethod
    def parse_url(cls, url):
        """Parse an Agave files resource URI into storageSystem and filePath
        """
        # TODO - Move implementation down to agavepy.utils
        # Agave URI
        if url.startswith('agave://'):
            url = url.replace('agave://', '', 1)
            parts = url.split('/')
            return parts[0], '/' + '/'.join(parts[1:])
        # Agave media URL
        elif url.startswith('https://'):
            url = url.replace('https://', '')
            parts = url.split('/')
            if parts[1] == 'files' and parts[3] == 'media':
                return parts[5], '/'.join(parts[6:])
        else:
            raise InvalidValue(
                '{0} not a valid Agave URI or HTTP URL'.format(url))

    def validate(self, url, permissive=False):
        try:
            self.parse_url(url)
            return True
        except Exception:
            if permissive:
                return False
            else:
                raise


class FilesURI(AgaveURI):
    def get_value(self, parsed_args, agave=None):
        uri = parsed_args.files_uri
        self.validate(uri)
        if uri.startswith('agave://'):
            system, path = self.parse_url(uri)
        api_server = agave.api_server
        if not api_server.endswith('/'):
            api_server = api_server + '/'

        http_uri = '{0}files/v2/media/system/{1}{2}'.format(
            agave.api_server, system, path)
        return http_uri

    def extend_parser(self, parser):
        parser.add_argument(
            'files_uri',
            type=str,
            metavar='FILES_URI',
            help=
            'Files URI (agave://system/path|https://api_server/system/path)')
        return parser
