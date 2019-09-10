from .base import TaccApisCommandBase

__all__ = ['TaccApisOnlyBasic']


class TaccApisOnlyBasic(TaccApisCommandBase):
    """Base class for Tapis API commands accepting only HTTP Basic Authentication
    """
    def add_common_parser_arguments(self, parser):
        parser = super(TaccApisOnlyBasic,
                       self).add_common_parser_arguments(parser)
        parser.add_argument('-u',
                            '--username',
                            dest='username',
                            type=str,
                            help="{0} username".format(
                                self.constants.PLATFORM))
        parser.add_argument('-p',
                            '--password',
                            dest='password',
                            type=str,
                            help="{0} password".format(
                                self.constants.PLATFORM))
        return parser
