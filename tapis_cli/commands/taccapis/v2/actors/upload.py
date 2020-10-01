from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import (ActorIdentifier, ActorFileOrMessage,
                     ActorEnvironmentVariables)

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .models import Message

__all__ = ['ActorsUpload']


class ActorsUpload(ActorsFormatOne, ActorIdentifier, ActorFileOrMessage,
                   ActorEnvironmentVariables):

    HELP_STRING = 'Send an asynchronous binary message to an Actor'
    LEGACY_COMMMAND_STRING = 'abaco run'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    SYNCHRONOUS_EXECUTION = False
    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsUpload, self).get_parser(prog_name)
        parser = ActorIdentifier().extend_parser(parser)
        parser = ActorFileOrMessage().extend_parser(parser)
        parser = ActorEnvironmentVariables().extend_parser(parser)
        return parser

    def prepare_message(self, parsed_args):
        body, environment, headers = {}, {}, {}
        message = self.handle_binary_file_upload(parsed_args)
        body = message
        headers = {'Content-Type': 'application/octet-stream'}
        environment = ActorEnvironmentVariables().process_parsed_args(
            parsed_args)
        environment['_abaco_synchronous'] = self.SYNCHRONOUS_EXECUTION
        if self.client_extra_args.get('nonce', None) is not None:
            environment['x-nonce'] = self.client_extra_args['nonce']
        return (body, headers, environment)

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        msg = self.prepare_message(parsed_args)
        rec = self.tapis_client.actors.sendMessage(actorId=actor_id,
                                                   body=msg[0],
                                                   headers=msg[1],
                                                   environment=msg[2],
                                                   **self.client_extra_args)
        headers = self.render_headers(Message, parsed_args)
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
