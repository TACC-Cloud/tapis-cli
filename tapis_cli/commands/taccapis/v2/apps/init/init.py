import docker as dockerpy
import git
import os
from cookiecutter.main import cookiecutter
from slugify import slugify

from tapis_cli import settings
from tapis_cli.display import Verbosity
from tapis_cli.utils import (seconds, milliseconds, print_stderr)
from tapis_cli.project_ini.mixins import AppIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.commands.taccapis.v2.apps.create import AppsCreate
from tapis_cli.clients.services.mixins import (WorkingDirectoryOpt,
                                               UploadJSONTemplate, DockerPy)
from tapis_cli.commands.taccapis.v2.files.helpers import manage, upload

from ..formatters import AppsFormatMany
from .. import API_NAME, SERVICE_VERSION
from ..helpers import pems
from . import templates

__all__ = ['AppsInit']

# class WorkflowFailed(Exception):
#     pass

# WORKFLOW
# accept URI, PROJECT, NAME, DESCRIPTION, PATH
# cookiecutter URI PROJECT => directory call NAME
# cd into NAME
# write project.ini#app.description
# write project.ini#docker.namespace,repo,tag?
# git init
# git config (user.name, user.email)
# (if possible and opted for - create remote; remote add origin; write project.ini#git.remote,name)


class AppsInit(AppsFormatMany):
    """Initialize a new Tapis app project.
    """

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    config = None
    document = None
    results = []
    messages = []
    exceptions = []
    passed_vals = {}

    # Workflow control flags
    git_init = True
    git_remote = False

    def get_parser(self, prog_name):
        parser = super(AppsInit, self).get_parser(prog_name)
        # Values for configuring the project itself
        parser.add_argument('project_name',
                            type=str,
                            metavar='<name>',
                            help='Project name')
        parser.add_argument('output_dir',
                            metavar='output_directory',
                            default='.',
                            nargs='?',
                            type=str,
                            help='Output directory (optional)')
        parser.add_argument('--description',
                            type=str,
                            dest='project_description',
                            metavar='<description>',
                            help='Project description')
        parser.add_argument('--version',
                            type=str,
                            dest='project_version',
                            default='0.0.1',
                            metavar='<version>',
                            help='Project version')

        # Coordinates for CookieCutter assets
        parser.add_argument('--repo',
                            type=str,
                            dest='source_repo',
                            default=templates.COOKIECUTTER_URI,
                            metavar='<uri>',
                            help='CookieCutter Repo ({})'.format(
                                templates.COOKIECUTTER_URI))
        parser.add_argument('--checkout',
                            type=str,
                            dest='source_checkout',
                            default=templates.CHECKOUT,
                            metavar='<checkout>',
                            help='CookieCutter Branch/Tag/Commit ({})'.format(
                                templates.CHECKOUT))
        parser.add_argument('--template',
                            type=str,
                            dest='source_dir',
                            default=templates.DIRECTORY,
                            metavar='<template>',
                            help='CookieCutter Template ({})'.format(
                                templates.DIRECTORY))

        # Override specific workflow actions
        return parser

    def take_action(self, parsed_args):
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

        # From settings
        extra_context[
            'docker_namespace'] = settings.TAPIS_CLI_REGISTRY_NAMESPACE

        # Generate project from template
        try:
            cookiecutter(parsed_args.source_repo,
                         no_input=True,
                         extra_context=extra_context,
                         output_dir=parsed_args.output_dir,
                         directory=parsed_args.source_dir,
                         checkout=parsed_args.source_checkout)
            self.messages.append('Created project at {0}'.format(project_path))
        except Exception as exc:
            self.exceptions.append(str(exc))

        # Attempt to set up project as git repo
        try:
            if settings.TAPIS_CLI_PROJECT_GIT_INIT:
                r = git.Repo.init(project_path)
                self.messages.append('Initialized git repo')
                if settings.TAPIS_CLI_PROJECT_GIT_FIRST_COMMIT:
                    add_files = os.listdir(project_path)
                    for af in add_files:
                        r.index.add([af])
                    r.index.commit('Automated first commit by Tapis CLI')
                else:
                    self.messages.commit('Skipped automated first commit')
                # Placeholder for create and set remote
                # Placeholder for push
            else:
                self.messages.append('Skipped initializing git repo')
        except Exception as exc:
            self.exceptions.append(str(exc))

        return (tuple(), tuple())
