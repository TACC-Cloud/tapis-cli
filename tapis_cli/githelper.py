"""Get details about project's git repository at runtime"""
import subprocess
# Portable and does not introduce any dependencies

__all__ = ['get_git_revision_hash', 'get_git_revision_short_hash',
           'get_git_remote']

def get_git_revision_hash():
    return subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']).decode().strip()

def get_git_revision_short_hash():
    return subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

def get_git_remote(name='origin'):
    return subprocess.check_output(
        ['git', 'remote', 'get-url', name],
        stderr=subprocess.DEVNULL).decode().strip()
