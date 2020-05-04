import sys
from agavepy.agave import AgaveError
from . import API_NAME, SERVICE_VERSION
from .submit import ActorsSubmit
from .mixins import ActorIdentifier

__all__ = ['ActorsRun']


class ActorsRun(ActorsSubmit):
    HELP_STRING = 'Send a message to an Actor and await response'
    LEGACY_COMMMAND_STRING = 'abaco run'
    SYNCHRONOUS_EXECUTION = True
    ACCEPT_NONCE = True

    def get_parser(self, prog_name):
        parser = super(ActorsRun, self).get_parser(prog_name)
        parser.add_argument('-O',
                            dest='output',
                            default=sys.stdout,
                            help='Output destination (default: STDOUT)')
        parser.add_argument('--binary',
                            action='store_true',
                            help='Treat output as binary data')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier().get_identifier(parsed_args)
        msg = self.prepare_message(parsed_args)
        resp = None
        try:
            API_PATH = '{0}/messages'.format(actor_id)
            self.requests_client.setup(API_NAME, SERVICE_VERSION, API_PATH)
            # Expecting a binary response
            resp = self.requests_client.post(params=msg[1], json=msg[0])
        except Exception as err:
            raise AgaveError('Message failed or timed out: {0}'.format(err))

        try:
            of = None
            if parsed_args.output == sys.stdout:
                print(resp.decode('utf-8'))
            elif parsed_args.binary:
                of = open(parsed_args.output, 'wb')
                of.write(resp)
                of.close()
            else:
                of = open(parsed_args.output, 'w')
                of.write(resp.decode('utf-8'))
                of.close()
        except Exception:
            raise

        sys.exit(0)
