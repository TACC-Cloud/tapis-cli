"""Exposes project and package metadata in a rationalized form
"""
import os.path
import re
from pkg_resources import get_distribution
from . import githelper

MAPPINGS = [('Name', 'title'), ('Summary', 'summary'), ('Home-page', 'uri'),
            ('Author', 'author'), ('Author-email', 'email'),
            ('Maintainer-email', 'help')]

OTHERS = [('Copyright', '2019 Texas Advanced Computing Center'),
          ('License', 'BSD-3'), ('Project', 'Tapis CLI')]

__all__ = ['About']


class About(object):
    def __init__(self, name='tapis_cli'):
        # Read from setup.cfg [metadata]
        dst = get_distribution(name)
        lines = dst.get_metadata_lines(dst.PKG_INFO)
        found = list()
        for line in lines:
            for metadata_name, attribute in MAPPINGS:
                if re.match('{}:'.format(metadata_name), line):
                    name, value = line.split(':', 1)
                    setattr(self, attribute, value.strip())
                    found.append(metadata_name)
                    break
                elif metadata_name not in found:
                    setattr(self, attribute, None)
        # extension metadata
        for other_name, value in OTHERS:
            setattr(self, other_name.lower(), value)
        # git commit if available
        try:
            commit = githelper.get_git_revision_short_hash()
        except Exception:
            commit = 'latest'
        setattr(self, 'git_commit', commit)
        # git remote if available
        try:
            remote = githelper.get_git_remote()
        except Exception:
            remote = None
        setattr(self, 'git_uri', remote)
