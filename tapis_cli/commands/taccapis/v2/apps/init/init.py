import docker as dockerpy
# import git
import os
from cookiecutter.main import cookiecutter

from tapis_cli import settings
from tapis_cli.display import Verbosity
from tapis_cli.utils import (seconds, milliseconds, print_stderr)
from tapis_cli.project_ini.mixins import AppIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.commands.taccapis.v2.apps.create import AppsCreate
from tapis_cli.clients.services.mixins import (WorkingDirectoryOpt,
                                               UploadJSONTemplate, DockerPy)
from tapis_cli.commands.taccapis.v2.files.helpers import manage, upload
from tapis_cli.utils import slugify

from ..formatters import AppsFormatManyUnlimited
from .. import API_NAME, SERVICE_VERSION
from ..helpers import pems
from . import templates

__all__ = ['AppsInit']

# class WorkflowFailed(Exception):
#     pass

# WORKFLOW
# accept URI, PROJECT, NAME, HELP_STRING, PATH
# cookiecutter URI PROJECT => directory call NAME
# cd into NAME
# write project.ini#app.description
# write project.ini#docker.namespace,repo,tag?
# git init
# git config (user.name, user.email)
# (if possible and opted for - create remote; remote add origin; write project.ini#git.remote,name)


class AppsInit(AppsFormatManyUnlimited):

    HELP_STRING = 'Initialize a new Tapis App project'
    LEGACY_COMMMAND_STRING = 'apps-init'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

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
        parser = super(AppsInit, self).get_parser(prog_name)
        parser.add_argument('-R',
                            '--dry-run',
                            dest='init_dry_run',
                            action='store_true')
        rungrp = parser.add_argument_group('Project Parameters')
        # Values for configuring the project itself
        rungrp.add_argument('project_name',
                            type=str,
                            metavar='STRING',
                            help='App name')
        rungrp.add_argument('output_dir',
                            metavar='output_directory',
                            default='.',
                            nargs='?',
                            type=str,
                            help='Output directory (optional)')
        rungrp.add_argument('--app-label',
                            type=str,
                            dest='project_label',
                            metavar='STRING',
                            help='Human-readable label')
        rungrp.add_argument('--app-description',
                            type=str,
                            dest='project_description',
                            metavar='STRING',
                            help='One-sentence description')
        rungrp.add_argument('--app-version',
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

    def take_action(self, parsed_args):
        self._take_action_init(parsed_args)
        return (tuple(self.headers), tuple(self.messages))
