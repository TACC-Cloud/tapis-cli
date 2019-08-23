from ....oauth import BearerTokenFormatOne, BearerTokenFormatMany

__all__ = ['GitlabTokenFormatOne', 'GitlabTokenFormatMany']


def add_common_arguments(parser):
    return parser


class GitlabTokenFormatOne(BearerTokenFormatOne):
    """Gitlab HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(GitlabTokenFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class GitlabTokenFormatMany(BearerTokenFormatMany):
    """Gitlab HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(GitlabTokenFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
