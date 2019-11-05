"""Mix-ins used to add defined behaviors to Tapis CLI commands
"""
import argparse
import json
import os
import sys
import validators

from agavepy.agave import Agave

from cliff.command import Command
from cliff.hooks import CommandHook
from cliff.app import App

from tapis_cli import constants
from tapis_cli.display import Verbosity
from tapis_cli.utils import serializable

__all__ = [
    'OptionNotImplemented', 'AppVerboseLevel', 'JsonVerbose',
    'ServiceIdentifier', 'UploadJsonFile', 'AgaveURI', 'JobsUUID',
    'RemoteFilePath', 'LocalFilePath', 'Username', 'InvalidIdentifier',
    'OptionalLocalFilePath', 'InvalidValue', 'URL', 'PostItsIdentifier',
    'NotificationsUUID', 'TapisEntityUUID', 'OptionalTapisEntityUUID',
    'MetadataUUID'
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


class ParserExtender(object):
    def extend_parser(self, parser):
        # When sublcassing: DO NOT FORGET TO RETURN PARSER
        return parser

    def preprocess_args(self, parsed_args):
        # When sublcassing: DO NOT FORGET TO RETURN PARSED_ARGS
        return parsed_args

    def render_field(self, key, value, formatter=None):
        return key, value

    def validate(self, value, permissive=True):
        """Placeholder to implement validation of a value passed
        via a ParserExtender
        """
        return True


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
        else:
            raise InvalidValue('{0} not a valid Agave URL or URI'.format(url))

    def validate(self, url, permissive=False):
        try:
            self.parse_url(url)
            return True
        except Exception:
            if permissive:
                return False
            else:
                raise


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

    @classmethod
    def arg_display(cls, id_value):
        return '<{0}_id>'.format(id_value).lower()

    @classmethod
    def arg_metavar(cls, id_value):
        return cls.arg_display(id_value)

    @classmethod
    def arg_help(cls, id_value):
        if not cls.optional:
            return '{0} {1}'.format(id_value, cls.id_type)
        else:
            return 'Optional {0} {1}'.format(id_value, cls.id_type)

    def extend_parser(self, parser):
        id_value = getattr(self, 'service_id_type')
        if id_value is not None:
            arg_display = '<{0}_id>'.format(id_value).lower()
        if self.optional:
            nargs = '?'
        else:
            nargs = None
        if id_value is not None:
            parser.add_argument('identifier',
                                type=str,
                                nargs=nargs,
                                metavar=self.arg_metavar(id_value),
                                help=self.arg_help(id_value))
        return parser

    def validate_identifier(self, identifier, permissive=True):
        return self.validate(identifier)

    def get_identifier(self, parsed_args, validate=False, permissive=False):
        identifier = None
        try:
            identifier = parsed_args.identifier
            self.validate_identifier(identifier)
        except Exception:
            if permissive:
                return False
            else:
                raise
        return identifier


class PostItsIdentifier(ServiceIdentifier):
    """Configures a Command to require a mandatory Post-it
    """
    def extend_parser(self, parser):
        parser.add_argument('identifier',
                            metavar='<postit_id>',
                            help='Post-it ID')
        return parser

    def validate_identifier(self, identifier, permissive=False):
        if len(identifier) == 32:
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidValue(
                    '{0} not a valid Post-it Identifier'.format(identifier))


class TapisEntityUUID(ServiceIdentifier):
    service_id_type = 'Tapis Entity'
    id_type = 'UUID'

    @classmethod
    def arg_display(cls, id_value):
        return '<{0}_uuid>'.format(id_value).lower()


class OptionalTapisEntityUUID(TapisEntityUUID):
    optional = True


class JobsUUID(TapisEntityUUID):
    """Configures a Command to require a mandatory Tapis job UUID
    """
    service_id_type = 'Job'

    def validate_identifier(self, identifier, permissive=False):
        if len(identifier) >= 36 and len(
                identifier) <= 40 and identifier.endswith('-007'):
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidValue(
                    '{0} not a valid Job UUID'.format(identifier))


class MetadataUUID(TapisEntityUUID):

    service_id_type = 'Metadata'

    def validate_identifier(self, identifier, permissive=False):
        if identifier.endswith('-012'):
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidIdentifier(
                    '{0} not a valid metadata UUID'.format(identifier))


class NotificationsUUID(TapisEntityUUID):
    """Configures a Command to require a mandatory Tapis notification UUID
    """
    service_id_type = 'Notification'

    def validate_identifier(self, identifier, permissive=False):
        if len(identifier) >= 36 and len(
                identifier) <= 40 and identifier.endswith('-011'):
            return True
        else:
            if permissive:
                return False
            else:
                raise InvalidValue(
                    '{0} not a valid Notification UUID'.format(identifier))


class RemoteFilePath(ParserExtender):
    """Configures a Command to accept an optional file path
    """
    def extend_parser(self, parser):
        parser.add_argument(
            'file_path',
            default='.',
            nargs='?',
            metavar='<file_path>',
            help='Optional file path relative to output directory')
        return parser


class LocalFilePath(ParserExtender):
    """Configures a Command to accept a local file path
    """
    def extend_parser(self, parser):
        parser.add_argument(
            'local_file_path',
            metavar='<file_path>',
            help='Path (relative to current working directory)')
        return parser


class OptionalLocalFilePath(ParserExtender):
    """Configures a Command to accept a local file path
    """
    def extend_parser(self, parser):
        parser.add_argument(
            'local_file_path',
            nargs='?',
            metavar='<file_path>',
            help='Optional path (relative to current working directory)')
        return parser


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
        if parsed_args.json_file_name == '-':
            document_source = sys.stdin
        elif parsed_args.json_file_name is not None and os.path.exists(
                parsed_args.json_file_name):
            document_source = open(parsed_args.json_file_name, 'rb')
        else:
            raise IOError('Unknown or inaccessible data source: {0}'.format(
                parsed_args.json_file_name))

        # Check JSON validity by loading and dumping it
        # TODO - factor validation into its own method so it can be overridden
        try:
            payload = json.load(document_source)
            serializable(payload)
            setattr(self, 'json_file_contents', payload)
        except Exception as exc:
            setattr(self, 'json_file_contents', None)
            raise ValueError('{0} was not valid JSON: {1}'.format(
                parsed_args.json_file_name, exc))


class Username(ParserExtender):
    """Configures a Command to accept an positional username
    """
    def extend_parser(self, parser):
        parser.add_argument('username',
                            metavar='<username>',
                            help='{0} username'.format(constants.PLATFORM))
        return parser


class URL(ParserExtender):
    """Configures a Command to require a mandatory 'url' positional parameter
    """
    def extend_parser(self, parser):
        parser.add_argument('url',
                            type=str,
                            metavar='<url>',
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
