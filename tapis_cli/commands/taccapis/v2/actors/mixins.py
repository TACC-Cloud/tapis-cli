from tapis_cli.clients.services.mixins import (ParserExtender,
                                               ServiceIdentifier)

__all__ = [
    'AliasIdentifier', 'ActorIdentifier', 'ExecutionIdentifier',
    'NonceIdentifier', 'WorkerIdentifier', 'GlobListFilter'
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
