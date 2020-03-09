import stringcase
from tapis_cli.clients.services.mixins import (ParserExtender, UploadJsonFile,
                                               TapisEntityUUID)

__all__ = [
    'UploadNotificationJson', 'NotificationsUUID', 'NotificationOptions'
]


class UploadNotificationJson(UploadJsonFile):
    optional = True


class NotificationsUUID(TapisEntityUUID):
    """Configures a Command to require a mandatory Tapis notification UUID
    """
    service_id_type = 'Notification'
    dest = 'notification_uuid'
    suffix = '-011'


class NotificationOptions(ParserExtender):
    def extend_parser(self, parser):
        parser.add_argument('-U',
                            '--url',
                            dest='url',
                            required=True,
                            metavar='URL',
                            help='URL destination for the notification')

        parser.add_argument(
            '-E',
            '--event',
            dest='event',
            action='append',
            metavar='EVENT',
            required=True,
            help='Event to subscribe to (can be specified multiple times)')

        parser.add_argument(
            '-P',
            '--persistent',
            action='store_true',
            help='Expire the notification after first occurrence of <event>')

        policy_group = parser.add_argument_group('retry policy settings')
        policy_group.add_argument(
            '--retry-strategy',
            dest='retry_strategy',
            choices=['IMMEDIATE', 'DELAYED', 'EXPONENTIAL'],
            help='Strategy for retrying failed delivery attempts')
        policy_group.add_argument(
            '--retry-delay',
            dest='retry_delay',
            type=int,
            metavar='INT',
            help=
            'Seconds to delay after the first failed notification attempt (max 1 day)'
        )
        policy_group.add_argument(
            '--retry-limit',
            dest='retry_limit',
            type=int,
            metavar='INT',
            help='Maximum number of retries before marking notification failed'
        )
        policy_group.add_argument(
            '--retry-rate',
            dest='retry_rate',
            type=int,
            metavar='INT',
            help=
            'Number of seconds between retries. A value of zero indicates another attempt should be made immediately.'
        )
        policy_group.add_argument(
            '--save-on-failure',
            action='store_true',
            help='Store failed attempts for future diagnostics')

        return parser

    def parsed_args_to_body(self, parsed_args, tapis_uuid):

        body = {'associatedUuid': tapis_uuid, 'url': parsed_args.url}

        # Handle 'event' as list
        event_names = [e.upper() for e in parsed_args.event]
        body['event'] = ','.join(event_names)

        # Handle persistent
        if parsed_args.persistent:
            body['persistent'] = True
        else:
            body['persistent'] = False

        policy = body.get('policy', {})
        BODY_PARAMS = [('retryStrategy', 'DELAYED'), ('retryDelay', 5),
                       ('retryLimit', 5), ('retryRate', 0),
                       ('saveOnFailure', True)]

        for key_name, default in BODY_PARAMS:
            attr_name = stringcase.snakecase(key_name)
            attr_value = getattr(parsed_args, attr_name)
            if attr_value is None:
                attr_value = default
            policy[key_name] = attr_value
        # raise SystemError(policy)
        # Local override - this should be handled by the service
        if policy['retryStrategy'] == 'IMMEDIATE':
            policy['retryDelay'] = 0

        body['policy'] = policy
        return body
