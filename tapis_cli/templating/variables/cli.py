from tapis_cli import PKG_NAME
from tapis_cli.__about__ import About
from pbr.version import VersionInfo

__all__ = ['key_values']


def key_values():
    cli = dict()
    about_info = About(PKG_NAME)
    version_info = VersionInfo(PKG_NAME)
    cli['tapis_cli_name'] = about_info.project
    cli['tapis_cli_version'] = version_info.version_string()
    return cli
