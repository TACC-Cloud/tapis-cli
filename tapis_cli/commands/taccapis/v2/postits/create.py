from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import FilesURI

from . import API_NAME, SERVICE_VERSION
from .models import PostIt, HTTP_METHODS, DEFAULT_LIFETIME, DEFAULT_MAX_USES
from .formatters import PostItsFormatOne

__all__ = ['PostItsCreate']


class PostItsCreate(PostItsFormatOne, FilesURI):

    HELP_STRING = 'Create a new Postit'
    LEGACY_COMMMAND_STRING = 'postits-create'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(PostItsCreate, self).get_parser(prog_name)
        parser = FilesURI.extend_parser(self, parser)
        parser.add_argument(
            '-L',
            '--lifetime',
            dest='lifetime',
            default=DEFAULT_LIFETIME,
            metavar='INT',
            help='Lifetime (default: {0} sec)'.format(DEFAULT_LIFETIME))
        parser.add_argument(
            '-m',
            '--max-uses',
            dest='max_uses',
            default=DEFAULT_MAX_USES,
            metavar='INT',
            help='Maximum redemptions (default: {0})'.format(DEFAULT_MAX_USES))
        parser.add_argument('-M',
                            '--http-method',
                            dest='http_method',
                            choices=HTTP_METHODS,
                            default='GET',
                            metavar='GET|POST',
                            help='HTTP method for URL (default: GET)')
        # parser.add_argument('-x',
        #                     '--token-username',
        #                     dest='token_username',
        #                     help='Impersonation username (requires admin privileges)')
        parser.add_argument('-N',
                            '--no-auth',
                            dest='no_auth',
                            action='store_true',
                            help='Do not pre-authenticate the URL')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)

        http_url = self.get_value(parsed_args, agave=self.tapis_client)
        body = {'url': http_url}

        if parsed_args.lifetime is not None:
            body['lifetime'] = parsed_args.lifetime
        if parsed_args.max_uses is not None:
            body['maxUses'] = parsed_args.max_uses
        if parsed_args.http_method is not None:
            body['method'] = parsed_args.http_method
        if parsed_args.no_auth is True:
            body['noauth'] = True

        headers = self.render_headers(PostIt, parsed_args)
        rec = self.tapis_client.postits.create(body=body)
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)

        # Extend response to show the full URL for the Post-It
        headers.append('postit_url')
        data.append(self.requests_client.build_url(rec.get('postit')))

        return (tuple(headers), tuple(data))
