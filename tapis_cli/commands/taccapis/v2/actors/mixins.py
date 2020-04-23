import os
from tapis_cli.utils import reserved_environment_vars
from tapis_cli.clients.services.mixins import (ParserExtender,
                                               ServiceIdentifier)

__all__ = [
    'AliasIdentifier', 'ActorIdentifier', 'ExecutionIdentifier',
    'NonceIdentifier', 'WorkerIdentifier', 'GlobListFilter',
    'ActorFileOrMessage', 'ActorEnvironmentVariables'
]


class AliasIdentifier(ServiceIdentifier):
    service_id_type = 'Alias'
    id_type = 'string'
    dest = 'alias_id'


class ActorIdentifier(ServiceIdentifier):
    service_id_type = 'Actor'
    dest = 'actor_id'


class ExecutionIdentifier(ServiceIdentifier):
    service_id_type = 'Execution'
    dest = 'execution_id'


class NonceIdentifier(ServiceIdentifier):
    service_id_type = 'Nonce'
    dest = 'nonce_id'


class WorkerIdentifier(ServiceIdentifier):
    service_id_type = 'Worker'
    dest = 'worker_id'


class GlobListFilter(ParserExtender):
    """Configures a list Command to accept a filter glob

    Sets 'parsed_args.list_filter'
    """
    FILTERABLE_KEYS = ['id']

    def extend_parser(self, parser):
        parser.add_argument('--filter',
                            metavar='GLOB',
                            dest='list_filter',
                            help='Filter by {}'.format(','.join(
                                self.FILTERABLE_KEYS)))
        return parser


class ActorFileOrMessage(ParserExtender):

    payload = None

    def extend_parser(self, parser):
        g = parser.add_mutually_exclusive_group(required=True)
        g.add_argument('-m',
                       '--message',
                       metavar='STRING',
                       type=str,
                       help='Message to send to the Actor')
        g.add_argument('-F',
                       '--file',
                       dest='file_name',
                       metavar='FILEPATH',
                       help='Text file containing Actor message')
        return parser

    def handle_file_upload(self, parsed_args):

        if parsed_args.message is not None:
            setattr(self, 'payload', parsed_args.message)
            return self.payload
        else:
            if parsed_args.file_name == '-':
                document_source = sys.stdin
            elif parsed_args.file_name is not None:
                document_source = os.path.join(self.getwd(),
                                               parsed_args.file_name)
            lf = open(document_source, 'r')
            setattr(self, 'payload', lf.read())
            return self.payload


class ActorEnvironmentVariables(ParserExtender):

    environment = {}

    def extend_parser(self, parser):
        parser.add_argument(
            '-e',
            dest='env_var',
            metavar='key=value',
            action='append',
            help=
            'Variable to send to the Actor (can be specified multiple times)')
        return parser

    def process_parsed_args(self, parsed_args):
        if parsed_args.env_var is not None:
            for arg in parsed_args.env_var:
                k, v = arg.split('=')
                if k in reserved_environment_vars():
                    raise KeyError(
                        'Variable "{0}" is reserved for internal use by Abaco'.
                        format(k))
                self.environment[k] = v
        return self.environment

    def validate(self, value, permissive=False):
        # Iterate thru list of envs
        # Reject MSG
        return True
