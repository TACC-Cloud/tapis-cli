from tapis_cli.display import Verbosity
from . import API_NAME, SERVICE_VERSION
from .models import Actor
from .formatters import ActorsFormatMany

__all__ = ['ActorsList']


class ActorsList(ActorsFormatMany):
    """List available Actors
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING_VERBOSE

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        headers = self.render_headers(Actor, parsed_args)
        # THIS IS THE API COMMAND
        results = self.tapis_client.actors.list()

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
