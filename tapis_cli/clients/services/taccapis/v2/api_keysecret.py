from .base import TaccApisCommandBase

__all__ = ['TaccApisKeySecretPassword', 'TaccApisKeySecretUsernamePassword']


class TaccApisKeySecretPassword(TaccApisCommandBase):
    """Parameterize Tapis API commands that accept API key/secret + password
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisKeySecretPassword,
                       self).add_common_parser_arguments(parser)
        parser.add_argument('-p',
                            '--password',
                            dest='password',
                            type=str,
                            help="{0} password".format(
                                self.constants.PLATFORM))
        parser.add_argument('-k',
                            '--client-key',
                            dest='api_key',
                            type=str,
                            help="{0} {1}".format(self.constants.PLATFORM,
                                                  self.constants.CLIENT_KEY))
        parser.add_argument(
            '-s',
            '--client-secret',
            dest='api_secret',
            type=str,
            help="{0} {1}".format(self.constants.PLATFORM,
                                  self.constants.CLIENT_SECRET))
        return parser


class TaccApisKeySecretUsernamePassword(TaccApisKeySecretPassword):
    """Parameterize Tapis API commands that accept API key/secret + username/password and/or token_username
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisKeySecretPassword,
                       self).add_common_parser_arguments(parser)
        parser.add_argument('-u',
                            '--username',
                            dest='username',
                            type=str,
                            help="{0} username".format(
                                self.constants.PLATFORM))
        parser.add_argument(
            '-x',
            '--token-username',
            dest='token_username',
            type=str,
            help="{0} token username (for impersonation)".format(
                self.constants.PLATFORM))
        return parser
