from tapis_cli.clients.services.mixins import (ParserExtender,
                                               ServiceIdentifier)

__all__ = ['ActorIdentifier' 'GlobListFilter']


class ActorIdentifier(ServiceIdentifier):
    service_id_type = 'Actor'
    dest = 'actor_id'


class GlobListFilter(ParserExtender):
    """Configures a list Command to accept a filter glob

    Sets 'parsed_args.list_filter'
    """
    FILTERABLE_KEYS = ['id']
    def extend_parser(self, parser):
        parser.add_argument('--filter',
                            metavar='<string>',
                            dest='list_filter',
                            help='Matches {}'.format(','.join(self.FILTERABLE_KEYS)))
        return parser
