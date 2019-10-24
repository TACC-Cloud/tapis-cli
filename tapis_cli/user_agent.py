from tapis_cli.main import PKG_NAME, About, VersionInfo

__all__ = ['user_agent']


def user_agent():
    """Generate a custom user-agent string for Tapis CLI
    """
    ab = About(PKG_NAME)
    vers = VersionInfo(PKG_NAME)
    ua = '{}/{}#{}'.format(ab.title, vers.version_string(), ab.git_commit)
    return ua
