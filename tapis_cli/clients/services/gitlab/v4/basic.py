from ....basic import BasicHTTPFormatOne

__all__ = ['GitlabBasicFormatOne']

def add_common_arguments(parser):
    return parser

class GitlabBasicFormatOne(BasicHTTPFormatOne):
    """Gitlab HTTP+Basic Record Display
    """
    def get_parser(self, prog_name):
        parser = super(GitlabBasicFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
