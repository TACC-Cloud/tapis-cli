import json
import os
import re
import sys

from tapis_cli import settings
from tapis_cli.display import Verbosity
from tapis_cli.utils import (seconds, milliseconds, print_stderr, parse_uri,
                             prompt, prompt_boolean, num)
from tapis_cli.settings.helpers import parse_boolean
from tapis_cli.clients.services.mixins import AgaveURI
from tapis_cli.project_ini.mixins import AppIniArgs, DockerIniArgs, GitIniArgs
from tapis_cli.clients.services.mixins import (WorkingDirectoryOpt)
from tapis_cli.commands.taccapis.v2.apps.mixins import AppIdentifier
from tapis_cli.utils import slugify

from ..formatters import JobsFormatManyUnlimited
from .. import API_NAME, SERVICE_VERSION
from .job import JOB_TEMPLATE

__all__ = ['JobsInit', 'DEFAULT_JOB_RUNTIME']

DEFAULT_JOB_RUNTIME = '01:00:00'


class JobsInit(JobsFormatManyUnlimited, AppIdentifier):

    HELP_STRING = 'Create a Job document for the specified App'
    LEGACY_COMMMAND_STRING = 'jobs-template'

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
        parser.add_argument('--interactive',
                            action='store_true',
                            help='Prompt for configuration and parameters')
        parser.add_argument(
            '--all',
            dest='all_fields',
            action='store_true',
            help='Include optional inputs and parameters in template')
        parser.add_argument('--name',
                            dest='job_name',
                            metavar='NAME',
                            help='Job name')
        parser.add_argument('--queue',
                            dest='queue_name',
                            metavar='QUEUE',
                            help='Queue')
        parser.add_argument('--duration',
                            dest='max_run_time',
                            metavar='HH:MM:SS',
                            help='Maximum run time (01:00:00)')

        # nopts = parser.add_mutually_exclusive_group()
        # nopts.add_argument('--cpus', dest='total_cpu_count', metavar='INT', help='CPUs')
        parser.add_argument('--nodes',
                            dest='node_count',
                            metavar='INT',
                            help='Compute nodes (1)')

        aopts = parser.add_mutually_exclusive_group()
        aopts.add_argument('--no-archive',
                           action='store_true',
                           help='Do not archive results')
        aopts.add_argument('--archive-uri',
                           type=str,
                           metavar='AGAVE_URI',
                           help='Path to archive results (agave://)')

        nopts = parser.add_mutually_exclusive_group()
        nopts.add_argument('--no-notify',
                           dest='no_notifications',
                           action='store_true',
                           help='Do not send job status notifications')
        nopts.add_argument('--notifications-uri',
                           type=str,
                           metavar='URI|EMAIL',
                           help='POST URL or email address for notifications')

        parser.add_argument('-O',
                            '--output',
                            dest='output',
                            default='',
                            metavar='PATH',
                            help='Output destination (STDOUT)')

        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        app_id = AppIdentifier.get_identifier(self, parsed_args)
        interactive = parsed_args.interactive

        app_def = {}
        exc_def = {}
        app_def = self.tapis_client.apps.get(appId=app_id)
        exc_def = self.tapis_client.systems.get(
            systemId=app_def.get('executionSystem'))

        # Intrepret parsed_args in light of contents of app and exec system definiitions
        # 1. allow --queue to over-ride app['defaultQueue']
        exc_queue_names = [q['name'] for q in exc_def['queues']]
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
        # TODO - Rewire so that we can check the queue name after prompting
        if interactive:
            print('Job configuration')
            print('-----------------')

        if interactive:
            queue_name = prompt('Queue ({0})'.format(
                '|'.join(exc_queue_names)),
                                queue_name,
                                allow_empty=False)

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
        # if interactive:
        #     queue_name = int(
        #         prompt('Memory (GB)', mem_per_node, allow_empty=False))
        if isinstance(mem_per_node, int):
            mem_per_node = str(mem_per_node) + 'GB'

        cpu_per_node = getattr(parsed_args, 'cpu_per_node',
                               app_def.get('defaultProcessorsPerNode', None))
        if cpu_per_node is None:
            cpu_per_node = sys_queue['maxProcessorsPerNode']
        # if interactive:
        #     cpu_per_node = int(
        #         prompt('CPU/Node', cpu_per_node, allow_empty=False))

        node_count = getattr(parsed_args, 'node_count',
                             app_def.get('defaultNodeCount', None))
        if node_count is None:
            # There is no default node count in a system queue definition
            node_count = 1
        if interactive:
            node_count = int(prompt('Nodes', node_count, allow_empty=False))

        # TODO - Validate that max_run_time is LTE sys_queue.maxRequestedTime
        max_run_time = getattr(parsed_args, 'max_run_time',
                               app_def.get('defaultMaxRunTime', None))
        if max_run_time is None:
            # max_run_time = sys_queue['maxRequestedTime']
            max_run_time = DEFAULT_JOB_RUNTIME
        if interactive:
            max_run_time = prompt('Run Time (max {0})'.format(
                sys_queue['maxRequestedTime']),
                                  max_run_time,
                                  allow_empty=False)
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
        if interactive:
            job_name = prompt('Job Name', job_name, allow_empty=False)

        # Build out the job definition
        job = JOB_TEMPLATE

        # Populate notifications config
        notify_job = not (parsed_args.no_notifications)
        if interactive:
            notify_job = prompt_boolean('Send status notifications',
                                        notify_job)
        if notify_job is True:
            try:
                if parsed_args.notifications_uri is not None:
                    nuri = parsed_args.notifications_uri
                else:
                    nuri = self.tapis_client.profiles.get()['email']
                if interactive:
                    nuri = prompt('Status notifications URI',
                                  nuri,
                                  allow_empty=False)
                notification = {'event': '*', 'persistent': True, 'url': nuri}
                job['notifications'].append(notification)
            except Exception:
                pass

        # Populate archiving config
        archive_job = not (parsed_args.no_archive)
        if interactive:
            archive_job = prompt_boolean('Archive job outputs', archive_job)
        job['archive'] = archive_job
        if archive_job:
            aui = getattr(parsed_args, 'archive_uri', None)
            if interactive:
                aui = prompt('Archive destination (Agave URI or leave empty)',
                             aui,
                             allow_empty=True)
                if aui == '':
                    aui = None
            if aui is not None:
                asys, apath = parse_uri(parsed_args.archive_uri)
                job['archiveSystem'] = asys
                job['archivePath'] = apath

        # Populate name and resource requirements
        job['name'] = job_name
        job['appId'] = app_id
        job['batchQueue'] = queue_name
        job['maxRunTime'] = max_run_time
        job['nodeCount'] = node_count
        job['processorsPerNode'] = cpu_per_node
        job['memoryPerNode'] = mem_per_node

        # Populate Inputs
        if interactive:
            print('Inputs')
            print('------')

        for inp in app_def.get('inputs', {}):
            if inp['value']['visible']:
                if inp['value']['required'] or parsed_args.all_fields is True:
                    job['inputs'][inp['id']] = inp['value'].get('default', '')
                    if interactive:
                        inp_label = inp['details']['label']
                        if inp_label is None or inp_label == '':
                            inp_label = inp['id']
                        resp = prompt(inp_label,
                                      job['inputs'][inp['id']],
                                      allow_empty=False)
                        # Validate URI
                        if re.search('^(agave://|http://|https://|ftp://)',
                                     resp):
                            job['inputs'][inp['id']] = resp
                        else:
                            raise ValueError(
                                'Input value {0} must be a URI'.format(resp))

        # Populate Parameters
        #
        # The behavior implemented here is different than the original bash
        # jobs-template in that we make no attempt to fake values for
        # parameters that don't have a default value
        if interactive:
            print('Parameters')
            print('----------')

        for prm in app_def.get('parameters', {}):
            if prm['value']['visible']:
                if prm['value']['required'] or parsed_args.all_fields is True:
                    job['parameters'][prm['id']] = prm['value'].get(
                        'default', '')
                    if job['parameters'][prm['id']] is None:
                        job['parameters'][prm['id']] = ''
                    if interactive:
                        prm_label = prm['details']['label']
                        if prm_label is None or prm_label == '':
                            prm_label = prm['id']
                        # Typecast and validate response
                        resp = prompt(prm_label,
                                      job['parameters'][prm['id']],
                                      allow_empty=False)
                        try:
                            if prm['value']['type'] in ('string',
                                                        'enumeration'):
                                resp = str(resp)
                            elif prm['value']['type'] in ('number'):
                                resp = num(resp)
                            elif prm['value']['type'] in ('bool', 'flag'):
                                resp = parse_boolean(resp)
                        except Exception:
                            raise ValueError(
                                'Unable to typecast {0} to type {1}'.format(
                                    resp, prm['value']['type']))
                        job['parameters'][prm['id']] = resp

        # Raw output
        outfile_dest = parsed_args.output
        if interactive:
            outfile_dest = prompt('Output destination',
                                  outfile_dest,
                                  allow_empty=True)
        if outfile_dest == '':
            of = sys.stdout
        else:
            of = open(outfile_dest, 'w')

        json.dump(job, fp=of, indent=2)
        sys.exit(0)
