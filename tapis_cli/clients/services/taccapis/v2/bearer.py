from ....oauth import BearerTokenFormatOne, BearerTokenFormatMany

__all__ = ['TaccApisFormatOne', 'TaccApisFormatMany']

def add_common_arguments(parser):
    return parser

class TaccApisFormatOne(BearerTokenFormatOne):
    """TACC APIs HTTP+Token Record Display
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatOne, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())

class TaccApisFormatMany(BearerTokenFormatMany):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        parser = super(TaccApisFormatMany, self).get_parser(prog_name)
        parser = add_common_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
