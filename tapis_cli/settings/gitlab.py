"""TACC Gitlab-specific CLI settings"""
import os
from .organization import TENANT_DNS_DOMAIN

__all__ = ['TACC_GITLAB_SERVER', 'TACC_GITLAB_URI']

TACC_GITLAB_SERVER = os.environ.get('TACC_GITLAB_SERVER',
                                    'git.' + TENANT_DNS_DOMAIN)
TACC_GITLAB_URI = 'https://' + TACC_GITLAB_SERVER
