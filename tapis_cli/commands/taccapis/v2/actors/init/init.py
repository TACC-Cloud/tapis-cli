import docker as dockerpy
# import git
import os
import requests
import urllib.parse
from cookiecutter.main import cookiecutter

from tapis_cli import settings
from tapis_cli.display import Verbosity
from tapis_cli.utils import (seconds, milliseconds, print_stderr)
from tapis_cli.project_ini.mixins import ActorIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.clients.services.mixins import (WorkingDirectoryOpt,
                                               UploadJSONTemplate, DockerPy)
from tapis_cli.commands.taccapis.v2.files.helpers import manage, upload
from tapis_cli.utils import slugify

from ..formatters import ActorsFormatManyUnlimited
from .. import API_NAME, SERVICE_VERSION
from . import templates

__all__ = ['ActorsInit']

# class WorkflowFailed(Exception):
#     pass

# WORKFLOW
# accept URI, PROJECT, NAME, HELP_STRING, PATH
# cookiecutter URI PROJECT => directory call NAME
# cd into NAME
# write project.ini#actor.description
# write project.ini#docker.namespace,repo,tag?
# git init
# git config (user.name, user.email)
# (if possible and opted for - create remote; remote add origin; write project.ini#git.remote,name)


class ActorsInit(ActorsFormatManyUnlimited):

    HELP_STRING = 'Initialize a new Tapis Actor project'
    LEGACY_COMMMAND_STRING = 'abaco-init'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    CATALOG_FILENAME = 'catalog.json'

    config = None
    document = None
    results = []
    headers = []
    messages = []
    exceptions = []
    passed_vals = {}

    # Workflow control flags
    git_init = True
    git_remote = False

    def get_parser(self, prog_name):
        parser = super(ActorsInit, self).get_parser(prog_name)
        parser.add_argument('-L',
                            '--list-templates',
                            dest='list_templates',
                            action='store_true',
                            help='List available templates and quit')
        parser.add_argument('-R',
                            '--dry-run',
                            dest='init_dry_run',
                            action='store_true')
        parser.add_argument('-O',
                            '--output-dir',
                            dest='output_dir',
                            metavar='DIRECTORY',
                            default='.',
                            type=str,
                            help='Output directory (default: .)')

        # Values for configuring the project itself
        rungrp = parser.add_argument_group('Actor Parameters')

        rungrp.add_argument('-N',
                            '--actor-name',
                            dest='project_name',
                            default='new_actor',
                            type=str,
                            metavar='STRING',
                            help='Actor name (default: new_actor)')
        rungrp.add_argument('--actor-label',
                            type=str,
                            dest='project_label',
                            metavar='STRING',
                            help='Human-readable label')
        rungrp.add_argument('--actor-description',
                            type=str,
                            dest='project_description',
                            metavar='STRING',
                            help='One-sentence description')
        rungrp.add_argument('--actor-version',
                            type=str,
                            dest='project_version',
                            metavar='N.N.N',
                            help='Semantic version')

        # Coordinates for CookieCutter assets
        cc_group = parser.add_argument_group('Source Template')
        cc_group.add_argument('--repo',
                              type=str,
                              dest='source_repo',
                              default=templates.COOKIECUTTER_URI,
                              metavar='URL',
                              help='CookieCutter Repo ({})'.format(
                                  templates.COOKIECUTTER_URI))
        cc_group.add_argument('--checkout',
                              type=str,
                              dest='source_checkout',
                              default=templates.CHECKOUT,
                              metavar='COMMIT',
                              help='Branch/Tag/Commit ({})'.format(
                                  templates.CHECKOUT))
        cc_group.add_argument('--template',
                              type=str,
                              dest='source_dir',
                              default=templates.DIRECTORY,
                              metavar='TEMPLATE',
                              help='Template name ({})'.format(
                                  templates.DIRECTORY))

        # Override specific workflow actions
        return parser

    def _take_action_init(self, parsed_args):
        # The setup and clone workflow is separated into a function in advance
        # of adding a separate workflow to fetch and retrieve a catalog of
        # project templates from the cookie cutter Github repo

        self.headers = ['stage', 'message']

        # Load parsed arguments into extra_context for sending
        # to cookiecutter
        extra_context = {}
        project_path = None
        # From CLI
        for cv in ('name', 'description', 'version'):
            val = getattr(parsed_args, 'project_' + cv, None)
            if val is not None:
                extra_context[cv] = val

        # safen name and predict final output path
        extra_context['project_slug'] = slugify(extra_context['name'],
                                                separator='_')
        project_path = os.path.join(parsed_args.output_dir,
                                    extra_context['project_slug'])
        self.messages.append(
            ('setup', 'Project path: {0}'.format(project_path)))

        # From settings
        extra_context[
            'docker_namespace'] = settings.TAPIS_CLI_REGISTRY_NAMESPACE
        # From settings
        extra_context['docker_registry'] = settings.TAPIS_CLI_REGISTRY_URL

        for k, v in extra_context.items():
            self.messages.append(
                ('setup', 'CookieCutter variable {0}={1}'.format(k, v)))

        if parsed_args.init_dry_run is True:
            self.messages.append(
                ('setup', 'Workflow stopped because this is a dry run'))
        else:
            # Generate project from template
            try:
                cookiecutter(parsed_args.source_repo,
                             no_input=True,
                             extra_context=extra_context,
                             output_dir=parsed_args.output_dir,
                             directory=parsed_args.source_dir,
                             checkout=parsed_args.source_checkout)
                self.messages.append(
                    ('clone', 'Project path: {0}'.format(project_path)))
            except Exception as exc:
                self.messages.append(('clone', str(exc)))

        return True

    def _take_action_list_templates(self, parsed_args):
        self.headers = ['id', 'name', 'description', 'level']
        # Compute Github raw file path from cookiecutter repo URL
        parsed = urllib.parse.urlparse(parsed_args.source_repo)
        branch = parsed_args.source_checkout
        cat_url = None

        # Convert https://github.com/TACC-Cloud/cc-tapis-v2-app.git to
        # https://raw.githubusercontent.com/TACC-Cloud/cc-tapis-v2-app/master/catalog.json
        if 'github.com' in parsed_args.source_repo:
            parsed = urllib.parse.urlparse(parsed_args.source_repo)
            # Strip trailing .git
            src_path = parsed.path.replace('.git', '')
            branch = parsed_args.source_checkout
            # Build URL
            cat_url = 'https://raw.githubusercontent.com{0}/{1}/{2}'.format(
                src_path, branch, self.CATALOG_FILENAME)
        else:
            raise WorkflowFailed(
                'Unable to list templates because source is not a Github URL')

        # Fetch catalog.json via HTTP/S
        try:
            resp = requests.get(cat_url)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            raise WorkflowFailed(Str(exc))

        for k, v in data.items():
            self.messages.append((k, v['name'], v['description'], v['level']))

        return True

    def take_action(self, parsed_args):

        # List templates -OR- start init functions
        if parsed_args.list_templates:
            self._take_action_list_templates(parsed_args)
        else:
            self._take_action_init(parsed_args)

        return (tuple(self.headers), tuple(self.messages))
