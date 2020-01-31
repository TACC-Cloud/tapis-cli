import datetime
import getpass
import json
import logging
import re

from tapis_cli import settings
from tapis_cli.commands.local.settings.set import settings_set
from tapis_cli.clients.services.mixins import ParserExtender
from tapis_cli.utils import prompt

__all__ = ['AuthRegistryInit', 'RegistryOpts']

logging.getLogger(__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ENV_PREFIX = 'TAPIS_CLI_'
VARS = ('REGISTRY_URL', 'REGISTRY_USERNAME', 'REGISTRY_PASSWORD',
        'REGISTRY_NAMESPACE')


class RegistryOpts(ParserExtender):
    def extend_parser(parser):
        """Configures a Command to accept container registry config
        """
        parser.add_argument('--registry-url',
                            metavar='<url>',
                            help='Registry URL')
        parser.add_argument('--registry-username',
                            metavar='<username>',
                            help='Registry username')
        parser.add_argument('--registry-password',
                            metavar='<password>',
                            help='Registry password')
        parser.add_argument('--registry-namespace',
                            metavar='<namespace>',
                            help='Registry namespace')
        return parser


def _read_current(parsed_args):
    # Inherit from passed '--interactive' flag
    current = {'interactive': getattr(parsed_args, 'interactive', False)}
    # Read from settings
    for ev in VARS:
        key_name = ENV_PREFIX + ev
        value = getattr(settings, key_name, None)
        current[key_name] = value
    # Read from parsed_args
    for av in VARS:
        key_name = ENV_PREFIX + av
        arg_name = av.lower()
        value = getattr(parsed_args, arg_name, None)
        if value is not None:
            current[key_name] = value

    # Force interactive mode if any values are empty
    for k, v in current.items():
        if v is None:
            current['interactive'] = True

    return current


def interactive(parsed_args, headers, results):
    """Interactively solicit configuration values
    """
    context = _read_current(parsed_args)

    if context['interactive']:
        print('Container registry access')
        print('=========================')

    for iv in VARS:
        prompt_name = iv.replace('_', ' ').title()
        key_name = ENV_PREFIX + iv
        header_name = iv.lower()

        if context['interactive']:
            if settings.redact.key_is_private(key_name):
                is_secret = True
            else:
                is_secret = False
            value = prompt(prompt_name, context[key_name], secret=is_secret)
        else:
            value = context[key_name]

        if value is not None and value != '':
            settings_set(key_name, value)

        headers.append(header_name)
        results.append(value)

    return (headers, results)
