from tapis_cli import githelper

__all__ = ['key_values']


def key_values():
    git = dict()
    git['git_remote'] = githelper.get_git_remote()
    git['git_revision_short_hash'] = githelper.get_git_revision_short_hash()
    git['git_revision_hash'] = githelper.get_git_revision_hash()
    return git
