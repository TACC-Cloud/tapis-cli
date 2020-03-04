import json
import os
import re
import sys
from slugify import slugify

from tapis_cli import settings
from tapis_cli.display import Verbosity
from tapis_cli.utils import (seconds, milliseconds, print_stderr, parse_uri)
from tapis_cli.clients.services.mixins import AgaveURI
from tapis_cli.project_ini.mixins import AppIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.clients.services.mixins import (WorkingDirectoryOpt)
from tapis_cli.commands.taccapis.v2.apps.mixins import AppIdentifier

from ..formatters import JobsFormatManyUnlimited
from .. import API_NAME, SERVICE_VERSION
from .job import JOB_TEMPLATE

__all__ = ['JobsInit', 'DEFAULT_JOB_RUNTIME']

DEFAULT_JOB_RUNTIME = '01:00:00'


class JobsInit(JobsFormatManyUnlimited, AppIdentifier):
    """Template a Tapis Job document for an App
    """

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    config = None
    document = None

    results = []
    messages = []
    exceptions = []
    passed_vals = {}

    def get_parser(self, prog_name):
        parser = super(JobsInit, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        parser.add_argument(
            '--all',
            dest='all_fields',
            action='store_true',
            help='Include optional inputs and parameters in template')
        parser.add_argument('--name',
                            dest='job_name',
                            metavar='<name>',
                            help='Job name')
        parser.add_argument('--queue',
                            dest='queue_name',
                            metavar='<queue>',
                            help='Queue')
        parser.add_argument('--duration',
                            dest='max_run_time',
                            metavar='<hh:mm:ss>',
                            help='Maximum run time HH:MM:SS (01:00:00)')

        # nopts = parser.add_mutually_exclusive_group()
        # nopts.add_argument('--cpus', dest='total_cpu_count', metavar='<int>', help='CPUs')
        parser.add_argument('--nodes',
                            dest='node_count',
                            metavar='<int>',
                            help='Compute nodes (1)')

        aopts = parser.add_mutually_exclusive_group()
        aopts.add_argument('--archive-uri',
                           type=str,
                           metavar='<agave_uri>',
                           help='Path to archive results (Files URI agave://)')
        aopts.add_argument('--no-archive',
                           action='store_true',
                           help='Do not archive results')

        # nopts = parser.add_mutually_exclusive_group()
        parser.add_argument('--no-notify',
                            dest='no_notifications',
                            action='store_true',
                            help='Do not send job status notifications')

        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        app_id = AppIdentifier.get_identifier(self, parsed_args)

        # passing this overrides no_archive
        # make options mututally exclusive
        archiveURI = None
        no_archive = False

        app_def = {}
        exc_def = {}
        app_def = self.tapis_client.apps.get(appId=app_id)
        exc_def = self.tapis_client.systems.get(
            systemId=app_def.get('executionSystem'))

        # Intrepret parsed_args in light of contents of app and exec system definiitions
        # 1. allow --queue to over-ride app['defaultQueue']
        queue_name = getattr(parsed_args, 'queue_name', None)
        if queue_name is None:
            queue_name = app_def.get('defaultQueue', None)

        # Get queue details for app execution system
        #
        # 1. Select either named queue -or- default queue
        # 2. ValueError if queue named and not found
        sys_queue = None
        if queue_name is not None:
            for q in exc_def['queues']:
                if q['name'] == queue_name:
                    sys_queue = q
                    break
        else:
            for q in exc_def['queues']:
                if q['default'] is True:
                    sys_queue = q
                    queue_name = sys_queue['name']
                    break
        if sys_queue is None:
            raise ValueError(
                'Job queue "{0}" does not exist on system "{1}"'.format(
                    queue_name, exc_def['id']))

        # Continue interpreting parsed_args
        #
        # Normally, we could just chain the getattr on parsed_args
        # and the successive chained get() to the app definition and
        # preferred system queue, but Tapis apps will actually return
        # an 'null' value for app.PROPERTY, which translates
        # to a value of None for job.PROPERTY.
        mem_per_node = getattr(parsed_args, 'memory_per_node',
                               app_def.get('defaultMemoryPerNode', None))
        if mem_per_node is None:
            mem_per_node = sys_queue['maxMemoryPerNode']
        if isinstance(mem_per_node, int):
            mem_per_node = str(mem_per_node) + 'GB'

        cpu_per_node = getattr(parsed_args, 'cpu_per_node',
                               app_def.get('defaultProcessorsPerNode', None))
        if cpu_per_node is None:
            cpu_per_node = sys_queue['maxProcessorsPerNode']

        node_count = getattr(parsed_args, 'node_count',
                             app_def.get('defaultNodeCount', None))
        if node_count is None:
            # There is no default node count in a system queue definition
            node_count = 1

        # TODO - Validate that max_run_time is LTE that sys_queue.maxRequestedTime
        max_run_time = getattr(parsed_args, 'max_run_time',
                               app_def.get('defaultMaxRunTime', None))
        if max_run_time is None:
            # max_run_time = sys_queue['maxRequestedTime']
            max_run_time = DEFAULT_JOB_RUNTIME
        # validate max_run_time
        if not re.search('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', max_run_time):
            raise ValueError(
                '{0} is not a valid job duration. Format must be HH:MM:SS'.
                format(max_run_time))

        # Safen provided job name or synthesize one if not provided
        job_name = getattr(parsed_args, 'job_name', None)
        if job_name is not None:
            job_name = slugify(job_name, separator='_')
        else:
            job_name = '{0}-job-{1}'.format(app_def['name'], milliseconds())

        # Build out the job definition
        job = JOB_TEMPLATE

        # Populate name and resource requirements
        job['name'] = job_name
        job['appId'] = app_id
        job['batchQueue'] = queue_name
        job['maxRunTime'] = max_run_time
        job['nodeCount'] = node_count
        job['processorsPerNode'] = cpu_per_node
        job['memoryPerNode'] = mem_per_node

        # Populate archiving config
        if getattr(parsed_args, 'no_archive', False) is True:
            job['archive'] = False
        else:
            job['archive'] = True
            aui = getattr(parsed_args, 'archive_uri', None)
            if aui is not None:
                asys, apath = parse_uri(parsed_args.archive_uri)
                job['archiveSystem'] = asys
                job['archivePath'] = apath

        # TODO Populate notifications config
        if parsed_args.no_notifications is False:
            try:
                email = self.tapis_client.profiles.get()['email']
                notification = {'event': '*', 'persistent': True, 'url': email}
                job['notifications'].append(notification)
            except Exception:
                pass

        # Populate Inputs
        for inp in app_def.get('inputs', {}):
            if inp['value']['visible']:
                if inp['value']['required'] or parsed_args.all_fields is True:
                    job['inputs'][inp['id']] = inp['value'].get('default', '')

        # Populate Parameters
        #
        # The behavior implemented here is different than the original bash
        # jobs-template in that we make no attempt to fake values for
        # parameters that don't have a default value
        for prm in app_def.get('parameters', {}):
            if prm['value']['visible']:
                if prm['value']['required'] or parsed_args.all_fields is True:
                    job['parameters'][prm['id']] = prm['value'].get(
                        'default', '')
                    if job['parameters'][prm['id']] is None:
                        job['parameters'][prm['id']] = ''

        # Raw output
        print(json.dumps(job, indent=4))
        sys.exit(0)
