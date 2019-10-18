import pytest

from tapis_cli.main import Tapis_App
from tapis_cli.commands.taccapis.v2 import apps

class TestAppsDescriptions(object):

    def test_apps_create_description(self):
        app = Tapis_App()
        cmd = apps.AppsCreate(app, None)
        assert cmd.get_description().startswith('Create a new app')

    def test_apps_disable_description(self):
        app = Tapis_App()
        cmd = apps.AppsDisable(app, None)
        assert cmd.get_description().startswith('Disable usage of an app')

    def test_apps_enable_description(self):
        app = Tapis_App()
        cmd = apps.AppsEnable(app, None)
        assert cmd.get_description().startswith('Restore usage for an App if disabled')

    def test_apps_history_description(self):
        app = Tapis_App()
        cmd = apps.AppsHistory(app, None)
        assert cmd.get_description().startswith('Show history of an App')

    def test_apps_list_description(self):
        app = Tapis_App()
        cmd = apps.AppsList(app, None)
        assert cmd.get_description().startswith('List the Apps catalog')

    def test_apps_publish_description(self):
        app = Tapis_App()
        cmd = apps.AppsPublish(app, None)
        assert cmd.get_description().startswith('Publish an App')

    def test_apps_search_description(self):
        app = Tapis_App()
        cmd = apps.AppsSearch(app, None)
        assert cmd.get_description().startswith('Search the Apps catalog')

    def test_apps_show_description(self):
        app = Tapis_App()
        cmd = apps.AppsShow(app, None)
        assert cmd.get_description().startswith('Show details for an App')

    def test_apps_unpublish_description(self):
        app = Tapis_App()
        cmd = apps.AppsUnpublish(app, None)
        assert cmd.get_description().startswith('Disable usage of a public App')

    def test_apps_update_description(self):
        app = Tapis_App()
        cmd = apps.AppsUpdate(app, None)
        assert cmd.get_description().startswith('Update an existing App')
