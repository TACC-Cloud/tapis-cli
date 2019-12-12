from . import BaseSchema


class Schema(BaseSchema):
    PROPERTIES = [('ssh_private_key', '~/.ssh/id_rsa', str,
                   'Current user SSH private key'),
                  ('ssh_public_key', '~/.ssh/id_rsa.pub', str,
                   'Current user SSH public key')]
