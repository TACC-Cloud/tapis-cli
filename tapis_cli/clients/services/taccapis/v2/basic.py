from ....basic import BasicHTTPFormatOne, BasicHTTPFormatMany

__all__ = ['TaccApisFormatOne', 'TaccApisFormatMany']


def add_common_arguments(parser):
    return parser


class TaccApisFormatOne(BasicHTTPFormatOne):
    """TACC APIs HTTP+Basic Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class TaccApisFormatMany(BasicHTTPFormatMany):
    """TACC APIs HTTP+Basic Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
