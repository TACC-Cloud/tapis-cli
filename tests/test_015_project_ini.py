import configparser
import os
import pytest
from tapis_cli import project_ini
from .data import project_ini as project_ini_data

def test_projects_ini_config_path_default():
    """Default path to project ini file is available by function
    """
    f = project_ini.config_path()
    assert f is not None
    assert os.path.basename(f) in project_ini.FILENAMES

def test_projects_ini_load_config():
    """ConfigParser can be loaded from default ini file
    """
    k = project_ini.load_config()
    assert isinstance(k, configparser.ConfigParser)

def test_projects_ini_load_config_dict():
    """ConfigParser can be loaded from default ini file
    """
    k = project_ini.load_config(as_dict=True)
    assert isinstance(k, dict)
    assert not isinstance(k, configparser.ConfigParser)

def test_projects_ini_load_config_by_path():
    """ConfigParser can be loaded by specifying a path
    """
    project_ini.load_config('tests/data/project_ini/project.ini')

def test_projects_ini_load_config_non_extistent_path():
    """If path to ini file is specified, it must exist
    """
    with pytest.raises(FileNotFoundError):
        project_ini.load_config('/this/is/fake/project.ini')

def test_projects_ini_load_config_invalid_name():
    """Ini file can only be (project.ini, app.ini, actor.ini)
    """
    with pytest.raises(ValueError):
        project_ini.load_config('tests/data/project_ini/invalid.ini')

def test_projects_ini_load_config_invalid_file_contents():
    """Cannot load arbitrary file type into ConfigParser
    """
    with pytest.raises(Exception):
        project_ini.load_config('tests/data/project_ini/non_ini/app.ini')

def test_projects_ini_save_config(temp_dir):
    """Ini file can be written to a named destination
    """
    k = project_ini.load_config('tests/data/project_ini/project.ini')
    project_ini.save_config(k, filename=os.path.join(temp_dir, 'project.ini'))

def test_projects_ini_save_config_invalid_name(temp_dir):
    """Destination must follow file naming conventions
    """
    k = project_ini.load_config('tests/data/project_ini/project.ini')
    with pytest.raises(ValueError):
        project_ini.save_config(k, filename=os.path.join(temp_dir, 'invald.ini'))

def test_projects_ini_update_config():
    """Can populate a config with a dict
    """
    k = project_ini.load_config('tests/data/project_ini/project.ini')
    project_ini.update_config(k, {'app': {'name': 'pytest'}})
    assert 'version' in k['app'], '"app" section missing from config'
    assert k['app']['name'] == 'pytest', '"version" option missing from "app" section'

def test_projects_ini_update_config_empty_dict():
    """Values dict can be empty, resulting in no change to config
    """
    k = project_ini.load_config('tests/data/project_ini/project.ini')
    project_ini.update_config(k, {})
    assert 'version' in k['app'], '"app" section missing from config'
    assert k['app']['name'] == 'fcs-etl', 'wrong name'

def test_projects_ini_update_config_invalid_dict():
    """Values dict must only contain sections and options defined by ini
    """
    k = project_ini.load_config('tests/data/project_ini/project.ini')
    with pytest.raises(KeyError):
        # Cannot add an option to an ini section
        project_ini.update_config(k, {'app': {'level': '9000'}})
    with pytest.raises(KeyError):
        # Cannot add a section to ini
        project_ini.update_config(k, {'candybar': {'name': 'Baby Ruth'}})

def test_projects_ini_key_values():
    """Config can be loaded and returned as key-values for templating
    """
    kv = project_ini.key_values()
    assert isinstance(kv, dict)

def test_projects_ini_key_values_by_path():
    """Config can be loaded and returned as key-values for templating
    """
    kv = project_ini.key_values('tests/data/project_ini/project.ini')
    assert isinstance(kv, dict)
    assert 'app' in kv

def test_projects_ini_generate_template():
    """Can generate a template config
    """
    template = project_ini.generate_template_ini()
    assert 'app' in template
    assert 'docker' in template

def test_projects_ini_generate_template_populated():
    """Can generate a pre-populated template config
    """
    template = project_ini.generate_template_ini({'app': {'name': 'tacotron'}})
    assert template['app']['name'] == 'tacotron'

def test_projects_ini_case_sensitive_load():
    k = project_ini.load_config('tests/data/project_ini/project.ini', as_dict=True)
    assert '_VAR_NAME_5' in k['environment']
    assert 'VAR_NAME_4' in k['environment']
