import datetime
import getpass
import json
import logging
import petname
import sys
import agavepy
from agavepy.agave import Agave, AgaveError
from agavepy import constants, tenants
from prettytable import PrettyTable
from requests.exceptions import HTTPError
from tapis_cli.display import Verbosity
from tapis_cli.constants import PLATFORM, TAPIS_AUTH_FAIL, TAPIS_AUTH_REJECT
from tapis_cli.utils import (fmtcols, prompt, get_hostname, get_public_ip,
                             get_local_username, prompt_boolean)
from tapis_cli.settings import TAPIS_DEFAULT_TENANT_ID, TAPIS_CLI_VERIFY_SSL
from tapis_cli.settings.helpers import os_environ_get_none
from tapis_cli import et
from tapis_cli.firstrun import firstrun

from . import API_NAME, SERVICE_VERSION
from .models import Token
from .formatters import CreateTokenFormatOne
from . import gitserver, registry

from .gitserver.init import GitServerOpts
from .registry.init import RegistryOpts

__all__ = ['AuthInit']

logging.getLogger(__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

CLIENT_PREFIX = '_cli'


class AuthInit(CreateTokenFormatOne, RegistryOpts, GitServerOpts):
    """Configure this host to use Tapis
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(AuthInit, self).get_parser(prog_name)

        parser.add_argument('--interactive',
                            action='store_true',
                            help='Prompt for all values')

        t = parser.add_mutually_exclusive_group()
        t.add_argument('--tenant-id',
                       dest='tenant_id',
                       help='{0} tenant ID'.format(PLATFORM))
        t.add_argument('--api-server',
                       dest='api_server',
                       help='{0} API server'.format(PLATFORM))

        parser.add_argument('--username',
                            dest='username',
                            help='{0} username'.format(PLATFORM))
        parser.add_argument('--password',
                            dest='password',
                            help='{0} password'.format(PLATFORM))

        parser.add_argument(
            '--client-name',
            dest='client_name',
            help='{0} client name. Leave empty to auto-generate.'.format(
                PLATFORM))

        parser = RegistryOpts.extend_parser(parser)
        parser = GitServerOpts.extend_parser(parser)

        cntl = parser.add_argument_group("Workflow Options")

        cntl.add_argument('--github',
                          dest='do_git',
                          action='store_true',
                          help='Configure Github credentials')
        cntl.add_argument('--no-dockerhub',
                          dest='do_docker',
                          action='store_false',
                          help='Do not configure DockerHub credentials')

        return parser

    def take_action(self, parsed_args):
        # Load what we can from credentials cache. Ultimately, if no
        # overrides are specified, the cached contents will be used to
        # populate the Tapis client.

        firstrun()
        interactive = parsed_args.interactive
        # Process overrides to ag_context provided by parsed_args
        mandate_username = False
        mandate_password = False
        mandate_git_reg = interactive

        if interactive:
            print('Configure Tapis API access:')
            print('===========================')

        # Fetch current values stored on disk into ag_context
        try:
            logger.debug('Reading from local Tapis environment')
            ag_context = Agave._read_current(agave_kwargs=True)
        except FileNotFoundError:
            # A very common case (all new tapis_cli installs, for instance), will
            # find NO cache file on disk. This must be recoverable, so set the
            # context to an empty dict
            logger.debug('Read from environment was unsuccessful')
            ag_context = {}
            mandate_username = True
            mandate_password = True

        # Inject optional password key
        ag_context['password'] = None

        # Ensure context has a setting for 'verify'. Default to env setting
        if 'verify' not in ag_context:
            ag_context['verify'] = TAPIS_CLI_VERIFY_SSL

        # Read in from parsed_args, updating ag_context

        # Process tenant override
        # Allow this to happen by either specifying --tenant-id or
        # --api-server. This will trigger the CLI to require user
        # credentials, which can be passed by argument or entered
        # interactively
        parsed_tenant_id = getattr(parsed_args, 'tenant_id', None)
        parsed_api_server = getattr(parsed_args, 'api_server', None)
        parsed_username = getattr(parsed_args, 'username', None)
        parsed_password = getattr(parsed_args, 'password', None)
        # Allow user to specify client name. Caveat emptor, though...
        parsed_client_name = getattr(parsed_args, 'client_name', None)

        # Allow tenant id OR api server to be provided, updating ag_context as appropriate
        # Regarding SSL verification: If the default behavior is to not verify, we will
        # not do verification when accessing the tenants API
        if parsed_tenant_id is not None:
            if ag_context.get('tenant_id', None) != parsed_tenant_id:
                # mandate_git_reg = True
                mandate_username = True
                mandate_password = True
                logger.info('Tenant changed. Credentials will be requested.')
            ag_context['tenant_id'] = parsed_tenant_id
            ag_context['api_server'] = agavepy.tenants.api_server_by_id(
                ag_context['tenant_id'], verify_ssl=TAPIS_CLI_VERIFY_SSL)
        elif parsed_api_server is not None:
            if ag_context.get('api_server', None) != parsed_api_server:
                # mandate_git_reg = True
                mandate_username = True
                mandate_password = True
                logger.info(
                    'API server changed. Credentials will be requested.')
            ag_context['api_server'] = parsed_api_server
            ag_context['tenant_id'] = agavepy.tenants.id_by_api_server(
                ag_context['api_server'], verify_ssl=TAPIS_CLI_VERIFY_SSL)

        # If interactive OR cannot establish tenant_id from cache
        # or args, prompt user to select one
        temp_tenant_id = ag_context.get('tenant_id', None)
        if temp_tenant_id is None or interactive:
            # Pick up default value for tenant_id from settings.TAPIS_DEFAULT_TENANT_ID
            if temp_tenant_id is None:
                temp_tenant_id = TAPIS_DEFAULT_TENANT_ID

            # Get list of tenants
            # tl = [t.get('code') for t in agavepy.tenants.list_tenants()]
            th = ['Name', 'Description', 'URL']
            tr = [[t.get('code'),
                   t.get('name'),
                   t.get('baseUrl')] for t in agavepy.tenants.list_tenants(
                       verify_ssl=TAPIS_CLI_VERIFY_SSL)]
            tl = [t[0] for t in tr]
            pt = PrettyTable()
            pt.field_names = ['Name', 'Description', 'URL']
            for rec in tr:
                pt.add_row(rec)
            print(pt)

            ag_context['tenant_id'] = prompt('Enter a tenant name',
                                             temp_tenant_id)
            if ag_context['tenant_id'] not in tl:
                raise ValueError(
                    'Error: "{0}" is not a valid tenant name'.format(
                        ag_context['tenant_id']))
            # Look up API server from tenant ID
            ag_context['api_server'] = agavepy.tenants.api_server_by_id(
                ag_context['tenant_id'], verify_ssl=TAPIS_CLI_VERIFY_SSL)

        # Prompt for SSL verification
        # From here on out in the workflow the user has indiciated a
        # specific preference re: SSL verification. So, we will use
        # their preference when communicating with APIs (clients, profiles)
        #
        # NOTE: Switching SSL behaviors might cause timeouts due to stale sessions
        if interactive:
            verify_ssl = ag_context.get('verify', TAPIS_CLI_VERIFY_SSL)
            ag_context['verify'] = prompt_boolean('Verify SSL connections',
                                                  verify_ssl)

        # Process --username argument
        if parsed_username is not None:
            # Force re-capture of password via argument or
            # interactive entry if username differs
            if ag_context.get(
                    'username',
                    None) != parsed_username and parsed_args.password is None:
                mandate_password = True
                logger.info('Username changed. Password will be required.')
            ag_context['username'] = parsed_username

        # Process --password argument
        if parsed_password is not None:
            ag_context['password'] = parsed_password

        # Prompt when interactive or username is reset or unavailable
        if interactive or (mandate_username and parsed_username is None):
            mandate_password = True
            ag_context['username'] = prompt('{0} username'.format(
                ag_context['tenant_id'], ag_context.get('username', None)),
                                            secret=False,
                                            allow_empty=False)

        # Prompt when interactive or username is reset or unavailable
        if interactive or (mandate_password and parsed_password is None):
            temp_password = prompt('{0} password for {1}'.format(
                ag_context['tenant_id'], ag_context['username']),
                                   parsed_password,
                                   secret=True,
                                   allow_empty=False)
            ag_context['password'] = temp_password

        # Password was provided. This indicates the Agave client should NOT
        # pass in any cached api_key, api_secret, and token, as it will be
        # interacting with the /clients service, which accepts Basic auth
        if ag_context['password'] is not None:
            ag_context['api_key'] = None
            ag_context['api_secret'] = None
            ag_context['access_token'] = None
            ag_context['refresh_token'] = None

        api_key = ag_context.get('api_key', None)
        ag = None

        # Generate client name
        if parsed_client_name:
            ag_context['client_name'] = parsed_client_name
        else:
            ag_context['client_name'] = '{0}-{1}-{2}-{3}'.format(
                CLIENT_PREFIX, ag_context['tenant_id'], ag_context['username'],
                get_hostname())

        # No client was loadable from the local system
        if api_key is None or api_key == '':
            logger.debug('clients.create: {0}'.format(
                ag_context['client_name']))
            create_context = {
                'api_server': ag_context['api_server'],
                'username': ag_context['username'],
                'password': ag_context['password'],
                'verify': ag_context['verify']
            }
            ag = Agave(**create_context)

            # Preflight activity: Get rid of existing client
            try:
                ag.clients.delete(clientName=ag_context['client_name'])
            except Exception:
                logger.debug('Tapis client was not deleted')
                pass

            try:
                ag.clients.create(
                    body={
                        'clientName':
                        ag_context['client_name'],
                        'description':
                        'Generated by {0}@{1} at {2}'.format(
                            get_local_username(), get_public_ip(),
                            datetime.datetime.utcnow().strftime(
                                "%Y-%m-%dT%H:%M:%SZ"))
                    })
            except Exception as err:
                logger.error('Tapis client was not created')
                raise AgaveError(TAPIS_AUTH_REJECT)
        else:
            # Client was cached - load it up
            logger.debug('Loading client from cache...')
            try:
                ag = Agave(**ag_context)
            except Exception as err:
                logger.error(
                    'Tapis client was not loaded from cache: {0}'.format(err))
                raise AgaveError(TAPIS_AUTH_FAIL)

        # Hit profiles service to check client
        try:
            ag.profiles.get()
        except Exception as err:
            logger.error(
                'Tapis client was unable to make an authenticated API call.')
            raise AgaveError(TAPIS_AUTH_FAIL)

        # Formulate a table view of key values for current session
        headers = [
            'tenant_id', 'username', 'api_key', 'access_token', 'expires_at',
            'verify'
        ]
        data = [
        # Coerce to string to avoid failures where a deepcopy
        # operation in Python's implementation of tuple() is
        # unable to accomodate copying properties of an Agave object
            str(ag.tenant_id),
            str(ag.username),
            str(ag.api_key),
            str(ag._token),
            str(ag.expires_at),
            str(ag.verify)
        ]

        # Show client name only if specified. Otherwise, end user really does
        # not need to see it
        if parsed_client_name:
            headers.append('client_name')
            data.append(ag_context['client_name'])

        # Extend headers and data with docker and git workflows
        if parsed_args.do_docker:
            (headers,
             data) = registry.init.interactive(parsed_args, headers, data,
                                               mandate_git_reg)
        if parsed_args.do_git:
            (headers,
             data) = gitserver.init.interactive(parsed_args, headers, data,
                                                mandate_git_reg)

        et.phone_home()
        return (tuple(headers), tuple(data))
