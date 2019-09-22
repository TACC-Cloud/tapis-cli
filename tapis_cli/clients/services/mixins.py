"""Mix-ins used to add defined behaviors to Tapis CLI commands
"""
import argparse
import json
from agavepy.agave import Agave

from cliff.command import Command
from cliff.hooks import CommandHook
from cliff.app import App
from tapis_cli.display import Verbosity

__all__ = [
    'AppVerboseLevel', 'JsonVerbose', 'ServiceIdentifier', 'UploadJsonFile',
    'AgaveURI'
]


class ParserExtender(object):
    def extend_parser(self, parser):
        # When sublcassing: DO NOT FORGET TO RETURN PARSER
        return parser

    def before_take_action(self, parsed_args):
        # When sublcassing: DO NOT FORGET TO RETURN PARSED_ARGS
        return parsed_args


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

    def before_take_action(self, parsed_args):
        parsed_args = super().before_take_action(parsed_args)
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
    service_id_type = 'Service'

    @classmethod
    def arg_display(cls, id_value):
        return '<{0}_id>'.format(id_value).lower()

    @classmethod
    def arg_metavar(cls, id_value):
        return cls.arg_display(id_value)

    @classmethod
    def arg_help(cls, id_value):
        return '{0} identifer'.format(id_value)

    def extend_parser(self, parser):
        id_value = getattr(self, 'service_id_type')
        if id_value is not None:
            arg_display = '<{0}_id>'.format(id_value).lower()
            if id_value is not None:
                parser.add_argument('identifier',
                                    type=str,
                                    metavar=self.arg_metavar(id_value),
                                    help=self.arg_help(id_value))
        return parser


class AgaveURI(ParserExtender):
    """Configures a Command to require a mandatory 'agave uri'
    positional parameter
    """
    def extend_parser(self, parser):
        parser.add_argument('agave_uri',
                            type=str,
                            metavar='<agave_uri>',
                            help='Agave files URI (agave://)')
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


class UploadJsonFile(ParserExtender):
    """Configures a client to accept and load a JSON file

    Adds -F and --file to a Command's parser. To load the designated file,
    the handle_file_upload() must then be called. JSON file contents will
    reside in self.json_file_contents.
    """
    json_loaded = dict()

    def extend_parser(self, parser):
        parser.add_argument('-F',
                            '--file',
                            dest='json_file_name',
                            type=str,
                            help='JSON payload file')
        return parser

    def handle_file_upload(self, parsed_args):
        with open(parsed_args.json_file_name, 'rb') as jfile:
            payload = json.load(jfile)
            setattr(self, 'json_file_contents', payload)
