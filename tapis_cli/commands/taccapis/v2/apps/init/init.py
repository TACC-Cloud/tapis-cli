import docker as dockerpy
import os

from tapis_cli.utils import (seconds, milliseconds, print_stderr)
from tapis_cli.project_ini.mixins import AppIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.commands.taccapis.v2.apps.create import AppsCreate
from tapis_cli.clients.services.mixins import (WorkingDirectoryArg,
                                               UploadJSONTemplate, DockerPy)
from tapis_cli.commands.taccapis.v2.files.helpers import manage, upload

from ..formatters import AppsFormatMany
from .. import API_NAME, SERVICE_VERSION
from ..helpers import pems

__all__ = ['AppsInit']


# class WorkflowFailed(Exception):
#     pass



class AppsInit(AppsFormatMany):
    """Initialize a new Tapis app project.
    """

    config = None
    document = None
    results = []
    messages = []
    passed_vals = {}

    # Workflow control flags
    clone = True
    git_init = True
    git_remote = False
