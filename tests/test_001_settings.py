import pytest
from .data import settings as settings_data

TEST_SETTING_NAME = 'TAPIS_CLI_LOG_LEVEL'
NONEXIST_SETTING_NAME = 'TAPIS_CLI_FLUX_CAPACITOR'

def test_settings_find_config():
    """Settings module can locate the env file
    """
    from tapis_cli import settings
    c = settings.find_config()
    assert c.endswith('.env')

def test_settings_load_config():
    """Settings module can try to load the env file
    """
    from tapis_cli import settings
    c = settings.load_config()
    assert c.endswith('.env')

def test_commands_settings_mixins_SettingName():
    from tapis_cli.commands.local.settings.mixins import SettingName
    n = SettingName()
    # Test inheritance behavior from ServiceIdentifier
    assert n.arg_display('value') == '<SETTING>'
    assert n.arg_metavar('value') == '<SETTING>'
    assert n.arg_help('value') == 'Tapis setting name'
    assert n.validate_identifier(TEST_SETTING_NAME)
    assert n.validate_identifier(NONEXIST_SETTING_NAME,
                                 permissive=True) is False
    # Private disallowed
    try:
        n.validate_identifier('_ENV_PATH')
    except ValueError:
        pass
    # Allow private settings name
    assert n.validate_identifier('_ENV_PATH', allow_private=True)


def test_commands_SettingsList(cliff_app, parsed_args_gen, fn_header_exists,
                      fn_key_exists):
    from tapis_cli.commands.local.settings import SettingsList
    parsed_args = parsed_args_gen()
    cmd = SettingsList(cliff_app, None)
    resp = cmd.take_action(parsed_args)
    # Expect 2 columns
    assert len(resp[0]) == 2
    assert fn_header_exists(resp[0], 'Setting')
    # Expect at least one row
    assert len(resp[1]) >= 1
    # Expect that _ENV_PATH is among the rows
    assert fn_key_exists(resp[1], '_ENV_PATH') is True
    # Case-sensitive
    assert fn_key_exists(resp[1], '_env_path') is False
    # Catch absence
    assert fn_key_exists(resp[1], 'AVOCADO_WINE') is False


def test_commands_SettingsGet(cliff_app, parsed_args_gen, fn_header_exists,
                     fn_key_exists):
    from tapis_cli.commands.local.settings import SettingsGet
    parsed_args = parsed_args_gen(identifier='TAPIS_CLI_LOG_LEVEL')
    cmd = SettingsGet(cliff_app, None)
    resp = cmd.take_action(parsed_args)
    # Expect 2 columns
    assert len(resp) == 2
    # # Expect exactly value
    assert len(resp[1]) == 1
