import json
import sys
from tapis_cli.display import Verbosity
from tapis_cli.utils import split_string, nrlist

from .. import API_NAME, SERVICE_VERSION
from ..formatters import ActorsFormatOne
from ..mixins import ActorIdentifier
from ..models import Actor

__all__ = ['ActorsBaseClass']


class ActorsBaseClass(ActorsFormatOne, ActorIdentifier):
    """Shared base class implementing actors create/update
    """

    CREATE_ONLY = False
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    config = {}

    def get_parser(self, prog_name):
        parser = super(ActorsBaseClass, self).get_parser(prog_name)
        parser = self.extend_parser(parser)
        return parser

    def extend_parser(self, parser):

        # Only accept actorId on update
        if self.CREATE_ONLY is False:
            parser = ActorIdentifier.extend_parser(self, parser)

        parser.add_argument('--repo',
                            dest='actor_repo',
                            type=str,
                            required=True,
                            help='Docker image repo for the Actor')

        if self.CREATE_ONLY:
            # Allow specification of name on create
            parser.add_argument('-n',
                                '--name',
                                dest='actor_name',
                                metavar='NAME',
                                type=str,
                                required=True,
                                help='Name of the Actor')

        parser.add_argument('-d',
                            '--description',
                            dest='actor_description',
                            metavar='DESCRIPTION',
                            type=str,
                            help='Plaintext description of the Actor')

        if self.CREATE_ONLY:
            # Stateful
            # This is an irrevocable decision when the actor is created
            sg = parser.add_mutually_exclusive_group()
            sg.add_argument('--stateful',
                            dest='actor_stateful',
                            action='store_true',
                            help='Actor will be stateful')
            sg.add_argument('--stateless',
                            dest='actor_stateless',
                            action='store_true',
                            help='Actor will be stateless [default]')

        # Hint
        # TODO - be able to set hints to []
        parser.add_argument('--hints',
                            type=str,
                            required=False,
                            dest='actor_hints',
                            help='Comma-separated list of keyword hints')

        # Privileged
        pg = parser.add_mutually_exclusive_group()
        pg.add_argument('--privileged',
                        dest='actor_privileged',
                        action='store_true',
                        help='Actor will have elevated privileges')
        pg.add_argument(
            '--unprivileged',
            dest='actor_unprivileged',
            action='store_true',
            help='Actor will not have elevated privileges [default]')

        # Tokens
        tg = parser.add_mutually_exclusive_group()
        tg.add_argument(
            '--tokens',
            dest='actor_tokens',
            action='store_true',
            help='Actor will request Tapis Oauth2 tokens [default]')
        tg.add_argument('--no-tokens',
                        dest='actor_notokens',
                        action='store_true',
                        help='Actor will not request Tapis Oauth2 tokens')

        # UID
        ug = parser.add_mutually_exclusive_group()
        ug.add_argument('--actor-uid',
                        dest='actor_containeruid',
                        action='store_true',
                        help='Actor will run as container UID')
        ug.add_argument('--user-uid',
                        dest='actor_useruid',
                        action='store_true',
                        help='Actor will run as the User UID [default]')

        # Environment variables
        eg = parser.add_mutually_exclusive_group()
        eg.add_argument(
            '-e',
            '--env',
            dest='actor_envs',
            action='append',
            metavar='KEY=VALUE',
            help='Actor environment variables (can be specified multiple times)'
        )
        eg.add_argument('-E',
                        '--env-file',
                        dest='actor_env_file',
                        help='Actor environment variables JSON file')

        parser.add_argument('--link',
                            type=str,
                            metavar='ACTOR_ID|ALIAS',
                            help='Actor ID or Alias event notifications')

        parser.add_argument('--webhook',
                            metavar='URL',
                            type=str,
                            help='URL for event notifications')

        # Cron schedule
        # See https://tacc-cloud.readthedocs.io/projects/abaco/en/latest/technical/messages.html#cron-schedule
        parser.add_argument(
            '--cron-schedule',
            dest='cron_schedule',
            metavar='SCHEDULE',
            type=str,
            help='Cron schedule (yyyy-mm-dd hh + <int> <time unit>)')
        # Cron active
        cg = parser.add_mutually_exclusive_group()
        cg.add_argument('--cron-on',
                        dest='cron_on_true',
                        action='store_true',
                        help='Actor cron is on')
        cg.add_argument('--cron-off',
                        dest='cron_on_false',
                        action='store_true',
                        help='Actor cron is off')

        parser.add_argument('--force',
                            action='store_true',
                            help='Force Abaco to update Actor container image')

        return parser

    def get_configuration(self, parsed_args, agave=None):
        """Returns specified Actor configuration from argparse inputs
        """
        config = {}

        # Name and description
        if getattr(parsed_args, 'actor_name', None) is not None:
            config['name'] = parsed_args.actor_name
        if getattr(parsed_args, 'actor_description', None) is not None:
            config['description'] = parsed_args.actor_description

        # Container image
        if parsed_args.actor_repo is not None:
            config['image'] = parsed_args.actor_repo

        # default is stateless=True
        if getattr(parsed_args, 'actor_stateful', None) is True:
            config['stateless'] = False
        else:
            config['stateless'] = True

        # default useContainerUid=False
        if parsed_args.actor_containeruid is True:
            config['useContainerUid'] = True
        else:
            config['useContainerUid'] = False

        # default token=True
        if parsed_args.actor_notokens is True:
            config['token'] = False
        else:
            config['token'] = True

        # Force update
        if parsed_args.force:
            config['force'] = True
        else:
            config['force'] = False

        # Hints
        hints = parsed_args.actor_hints
        if hints is not None:
            hints = nrlist(split_string(hints))
            config['hints'] = hints

        # Environment defaultEnvironment
        config['defaultEnvironment'] = self.get_envs(parsed_args)

        # Link
        if parsed_args.link is not None:
            config['link'] = parsed_args.link

        # Webhook
        if parsed_args.webhook is not None:
            config['webhook'] = parsed_args.webhook

        # Cron schedule
        cron_schedule = parsed_args.cron_schedule
        if cron_schedule is not None:
            config['cronSchedule'] = cron_schedule

        # Cron active
        if getattr(parsed_args, 'cron_on_true', None) is True:
            config['cronOn'] = True
        elif getattr(parsed_args, 'cron_on_false', None) is True:
            config['cronOn'] = False

        return config

    def get_envs(self, parsed_args):
        """Returns specified environment variables from CLI and file
        """
        if parsed_args.actor_env_file is not None:
            file_envs = self.get_envs_from_file(parsed_args.actor_env_file)
        else:
            file_envs = {}

        passed_envs = {}
        if parsed_args.actor_envs is not None:
            for e in parsed_args.actor_envs:
                k, v = e.split('=')
                passed_envs[k] = v

        # This merge order would allow passed environment vars to override contents of the file
        envs = {**file_envs, **passed_envs}

        return envs

    @classmethod
    def get_envs_from_file(cls, filename, decryption_key=None):
        # TODO - allow decryption with a public key (https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/)
        file_envs = json.load(open(filename, 'r'))
        return file_envs

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        config = self.get_configuration(parsed_args, agave=self.tapis_client)
        setattr(self, 'config', config)
        return (tuple(), tuple())
