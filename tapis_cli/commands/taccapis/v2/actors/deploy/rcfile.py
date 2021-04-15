"""Loads a legacy reactor.rc file as a config dictionary
"""
import configparser
import os
from tapis_cli.settings.helpers import parse_boolean

RC_FILENAME = 'reactor.rc'


def load_config(filename=RC_FILENAME, as_dict=False, permissive=True):
    """Return project configuration as ConfigParser or dict from reactor.rc
    """
    if filename is None:
        filename = config_path()
    else:
        # Fail if filename is passed but does not exist
        if not os.path.exists(filename):
            if permissive:
                return {}
            else:
                raise FileNotFoundError('{0} was not found'.format(filename))

    with open(filename, 'r') as rcfile:
        lines = rcfile.readlines()
        lines = [l.strip() for l in lines]

        actor = {}
        docker = {}
        config = {}
        kvdict = {}

        for l in lines:
            if not l.startswith('#') and not l.startswith(';'):
                keyval = l.split('=', 1)
                if len(keyval) == 2:
                    k = keyval[0].strip()
                    v = keyval[1].strip()
                    if v.startswith('"'):
                        v = v[1:]
                    if v.endswith('"'):
                        v = v[:-1]
                    kvdict[k] = v

        # Environment, Job, Git, Grants empty but must exist when reading from an .rc file
        config['environment'] = {}
        config['job'] = {}
        config['git'] = {}
        config['grants'] = {}

        # Actor basic config
        if 'REACTOR_NAME' in kvdict:
            actor['name'] = kvdict['REACTOR_NAME']
        if 'REACTOR_DESCRIPTION' in kvdict:
            actor['description'] = kvdict['REACTOR_DESCRIPTION']
        # if 'REACTOR_ALIAS' in kvdict:
        #     actor['alias'] = kvdict['REACTOR_ALIAS']

        # Config booleans
        if 'REACTOR_TOKENS' in kvdict:
            actor['token'] = parse_boolean(kvdict['REACTOR_TOKENS'])
        if 'REACTOR_PRIVILEGED' in kvdict:
            actor['privileged'] = parse_boolean(kvdict['REACTOR_PRIVILEGED'])
        if 'REACTOR_USE_UID' in kvdict:
            actor['use_container_uid'] = parse_boolean(
                kvdict['REACTOR_USE_UID'])
        # Note the 'not' here, which is needed because the key in project.ini is
        # actor.stateless not actor.stateful
        if 'REACTOR_STATEFUL' in kvdict:
            actor['stateless'] = not (parse_boolean(
                kvdict['REACTOR_STATEFUL']))

        # Cron features
        if 'REACTOR_CRON_SCHEDULE' in kvdict:
            actor['cronSchedule'] = kvdict['REACTOR_CRON_SCHEDULE']
        if 'REACTOR_CRON_ON' in kvdict:
            actor['cronOn'] = parse_boolean(kvdict('REACTOR_CRON_ON'))

        # Docker configuration
        if 'DOCKER_HUB_ORG' in kvdict:
            docker['namespace'] = kvdict['DOCKER_HUB_ORG']
        if 'DOCKER_IMAGE_TAG' in kvdict:
            docker['repo'] = kvdict['DOCKER_IMAGE_TAG']
        if 'DOCKER_IMAGE_VERSION' in kvdict:
            docker['tag'] = kvdict['DOCKER_IMAGE_VERSION']
        if 'DOCKERFILE' in kvdict:
            docker['dockerfile'] = kvdict['DOCKERFILE']

        if as_dict:
            if actor != {}:
                config['actor'] = actor
            if docker != {}:
                config['docker'] = docker
            return config
        else:
            cp = configparser.ConfigParser()
            if actor != {}:
                cp['actor'] = actor
            if docker != {}:
                cp['docker'] = docker
            return cp


def config_path(filename=None, working_directory=None):
    if filename is None:
        return RC_FILENAME
    else:
        return filename
