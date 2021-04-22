from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import UploadJSONTemplate

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsCreate']

# TODO - enforce use of create vs update by checking for existence of systemId


class SystemsCreate(SystemsFormatOne, UploadJSONTemplate):

    HELP_STRING = 'Create a new System'
    LEGACY_COMMMAND_STRING = 'systems-addupdate'

    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsCreate, self).get_parser(prog_name)
        parser = UploadJSONTemplate.extend_parser(self, parser)

        sg = parser.add_argument_group('SSH/SFTP Authentication Options')
        sg.add_argument('--login-username',
                        dest='login_username',
                        metavar='USERNAME',
                        type=str,
                        help='Username for SSH login on the System')
        sg.add_argument('--login-public-key',
                        dest='login_public_key',
                        metavar='FILE',
                        type=str,
                        help='Public key for SSH login on the System')
        sg.add_argument('--login-private-key',
                        dest='login_private_key',
                        metavar='FILE',
                        type=str,
                        help='Private key for SSH login on the System')
        sg.add_argument('--login-password',
                        dest='login_password',
                        metavar='PASSWORD',
                        type=str,
                        help='Password for SSH login on the System')

        sg.add_argument('--storage-username',
                        dest='storage_username',
                        metavar='USERNAME',
                        type=str,
                        help='Username for SFTP storage on the System')
        sg.add_argument('--storage-public-key',
                        dest='storage_public_key',
                        metavar='FILE',
                        type=str,
                        help='Public key for SFTP storage on the System')
        sg.add_argument('--storage-private-key',
                        dest='storage_private_key',
                        metavar='FILE',
                        type=str,
                        help='Private key for SFTP storage on the System')
        sg.add_argument('--storage-password',
                        dest='storage_password',
                        metavar='PASSWORD',
                        type=str,
                        help='Password for SFTP storage on the System')

        # Add in key arguments
        return parser

    def update_json_creds(self, parsed_args) -> None:
        """Updates system login and storage credentials in
        attr `json_file_contents` with command line arguments from
        `parsed_args`.
        """
        json_data = self.json_file_contents

        # System storage configuration via parsed_args
        if json_data.get('storage', {}).get('protocol', None) == 'SFTP':
            # Override username
            if parsed_args.storage_username is not None:
                json_data['storage']['auth'][
                    'username'] = parsed_args.storage_username
            # Overide keys or password
            if json_data.get('storage', {}).get('auth',
                                                {}).get('type',
                                                        None) == 'SSHKEYS':
                # Override SSH keys
                if parsed_args.storage_public_key is not None:
                    pubkey = open(parsed_args.storage_public_key,
                                  'r').read().strip()
                    json_data['storage']['auth']['publicKey'] = pubkey
                if parsed_args.storage_private_key is not None:
                    privkey = open(parsed_args.storage_private_key,
                                   'r').read().strip()
                    json_data['storage']['auth']['privateKey'] = privkey
            elif json_data.get('storage', {}).get('auth',
                                                  {}).get('type',
                                                          None) == 'PASSWORD':
                # Override password
                if parsed_args.storage_password is not None:
                    json_data['storage']['auth'][
                        'password'] = parsed_args.storage_password

        # System login configuration via parsed_args
        if json_data.get('login', {}).get('protocol', None) == 'SSH':
            # Override username
            if parsed_args.login_username is not None:
                json_data['login']['auth'][
                    'username'] = parsed_args.login_username
            # Overide keys or password
            if json_data.get('login', {}).get('auth',
                                              {}).get('type',
                                                      None) == 'SSHKEYS':
                # Override SSH keys
                if parsed_args.login_public_key is not None:
                    pubkey = open(parsed_args.login_public_key,
                                  'r').read().strip()
                    json_data['login']['auth']['publicKey'] = pubkey
                if parsed_args.login_private_key is not None:
                    privkey = open(parsed_args.login_private_key,
                                   'r').read().strip()
                    json_data['login']['auth']['privateKey'] = privkey
            elif json_data.get('login', {}).get('auth',
                                                {}).get('type',
                                                        None) == 'PASSWORD':
                # Override password
                if parsed_args.login_password is not None:
                    json_data['login']['auth'][
                        'password'] = parsed_args.login_password
        return None

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        self.update_json_creds(parsed_args)
        json_data = self.json_file_contents

        # Enroll the system
        headers = headers = self.render_headers(System, parsed_args)
        rec = self.tapis_client.systems.add(body=json_data)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
