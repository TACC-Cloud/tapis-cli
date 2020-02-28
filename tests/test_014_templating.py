import pytest
from .data import clients as clients_data

def test_render_template_undefined_var():
    """Empty variables are allowed in template after rendering
    """
    # Until the allow_undefined is actually implemented, empty variables will
    # not raise an error. Revisit this test when it is implemented.
    from tapis_cli.templating import render_template
    source = '{{ variable_a }} static'
    env = {'variable1': 'nonstatic', 'variable2': 'unstatic'}
    rendered = render_template(source, passed_vals=env)
    assert rendered is not None

def test_render_template_pass_dict():
    """Values will be rendered from a passed dict
    """
    from tapis_cli.templating import render_template
    source = '{{ variable1 }} static'
    env = {'variable1': 'nonstatic', 'variable2': 'unstatic'}
    rendered = render_template(source, passed_vals=env)
    assert 'nonstatic' in str(rendered)
    assert 'unstatic' not in str(rendered)

def test_render_template_passed_vals_supercede_builtin():
    """Values in a passed dict should override default/discovered values
    """
    from pbr.version import VersionInfo
    from tapis_cli import PKG_NAME
    from tapis_cli.templating import render_template

    version_info = VersionInfo(PKG_NAME)
    version_string = version_info.version_string()

    source = 'Tapis CLI version {{ tapis_cli_version }} is cool'
    env = {}
    rendered = render_template(source, passed_vals=env)
    assert version_string in str(rendered)

    # Pass over-ride value
    env = {'tapis_cli_version': 9000}
    rendered = render_template(source, passed_vals=env)
    assert '9000' in str(rendered)

def test_render_template_nested():
    """Nested values from a configparser instance should
    render as values not as the name of the section
    """
    from tapis_cli.templating import render_template
    source = 'App Name {{ app.name }} is cool'
    rendered = render_template(source, passed_vals={'app': {'name': 'abcdef'}})
    assert 'abcdef' in str(rendered)

def test_taccapis_api_client_init(tapis_active_client):
    """Test dynamic generation of Tapis-relevant templating data
    """
    from tapis_cli.clients.services.taccapis.v2 import TaccApiClient
    tac = TaccApiClient()
    tac.init_clients()
    tackv = tac.key_values()
    assert tackv['tenant_id'] is not None, 'No tenant ID'
    assert tackv['api_server'] is not None, 'No API server'
    assert tackv['email'] is not None, 'No email'
    assert tackv['first_name'] is not None, 'No first name'
    assert tackv['default_public_storage'] is not None, 'No default public storage system'

def test_command_key_values(tapis_active_client):
    from tapis_cli.clients.services.taccapis.v2 import TaccApiClient
    tac = TaccApiClient()
    tac.init_clients()
    tackv = tac.key_values()
    variables = list(tackv.keys())
    variables.sort()
    assert len(variables) > 0
