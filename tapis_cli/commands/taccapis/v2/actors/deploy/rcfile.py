"""Implements loading of legacy reactor.rc file as a config
"""
import os

# Other inis might exist but we will only actively try loading from these
FILENAMES = ['reactor.rc]
DEFAULT_FILENAME = 'reactor.rc'

TEMPLATE = '''
[docker]
namespace = {{ DOCKER_HUB_ORG}}
username = 
repo = {{ DOCKER_IMAGE_TAG }}
tag = {{ DOCKER_IMAGE_VERSION }}
dockerfile = 

[actor]
name = {{ REACTOR_NAME }}
description =
oauth_client = {{ REACTOR_TOKENS }}
stateless = True

'''

ACTOR_VARS = ['REACTOR_NAME', 'REACTOR_TOKENS']
DOCKER_VARS = ['DOCKER_HUB_ORG', 'DOCKER_IMAGE_TAG', 'DOCKER_IMAGE_VERSION']

def load_config(filename=None, as_dict=False):
    if filename is None:
        filename = config_path()
    else:
        # Fail if filename is passed but does not exist
        if not os.path.exists(filename):
            raise FileNotFoundError('{0} was not found'.format(filename))
    if os.path.basename(filename) in FILENAMES:
        pass

def config_path(filename=None, working_directory=None):
    if working_directory is None:
        working_directory = os.getcwd()

    if filename is not None:
        return filename
    else:
        for fname in FILENAMES:
            ipath = os.path.join(working_directory, fname)
            if os.path.exists(ipath):
                return ipath

        return os.path.join(working_directory, DEFAULT_FILENAME)
