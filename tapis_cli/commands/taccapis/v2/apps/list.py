from . import App
from . import AppsFormatMany
from . import SERVICE_VERSION, API_NAME

__all__ = ['AppsList']


class AppsList(AppsFormatMany):
    def get_parser(self, prog_name):
        parser = super(AppsFormatMany, self).get_parser(prog_name)
        # parser.add_argument(
        #     '--name',
        #     type=str,
        #     help='Filter to apps with <NAME>'
        # )
        # TODO - build parser arguments from schema.
        # TODO - convert camelCase -> camel_case -> --camel-case
        # TODO - Support --field (modifier) value like in Data Catalog

        parser.add_argument('-Q',
                            '--private',
                            action='store_false',
                            dest='public',
                            help='Only return private apps')
        parser.add_argument('-P',
                            '--public',
                            action='store_true',
                            dest='public',
                            help='Only return public apps')
        # parser.add_argument(
        #     '--system',
        #     type=str,
        #     help='Filter to apps on <SYSTEM>'
        # )
        return parser

    def take_action_swaggerpy(self, parsed_args):
        super().take_action(parsed_args)
        results = self.tapis_client.apps.list(
            limit=parsed_args.limit,
            offset=parsed_args.offset,
            publicOnly=parsed_args.publicOnly)
        # TODO - define this programmatically
        headers = [
            'id', 'name', 'version', 'revision', 'executionSystem',
            'shortDescription', 'isPublic', 'label', 'lastModified'
        ]
        records = []
        for rec in results:
            record = []
            for key in headers:
                record.append(rec.get(key, None))
            records.append(record)

        return (tuple(headers), tuple(records))

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        PARAMS = [('limit', 'limit'), ('offset', 'offset'),
                  ('public', 'public')]
        payload = {}
        for param, arg in PARAMS:
            val = getattr(parsed_args, arg, None)
            if val is not None:
                payload[param] = val
        results = self.requests_client.get_data(params=payload)
        # TODO - define this programmatically or at least w some degree of inheritance
        headers = [
            'id', 'name', 'version', 'revision', 'executionSystem',
            'shortDescription', 'isPublic', 'label', 'lastModified'
        ]
        records = []
        for rec in results:
            record = []
            for key in headers:
                record.append(rec.get(key, None))
            records.append(record)
        return (tuple(headers), tuple(records))
