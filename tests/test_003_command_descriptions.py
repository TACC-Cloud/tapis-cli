import pytest

from tapis_cli.main import Tapis_App
from tapis_cli.commands.taccapis.v2 import apps
from tapis_cli.commands.taccapis.v2 import metadata


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
        assert cmd.get_description().startswith(
            'Restore usage for an App if disabled')

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
        assert cmd.get_description().startswith(
            'Disable usage of a public App')

    def test_apps_update_description(self):
        app = Tapis_App()
        cmd = apps.AppsUpdate(app, None)
        assert cmd.get_description().startswith('Update an existing App')


class TestMetaDescriptions(object):
    def test_meta_create_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataCreate(app, None)
        assert cmd.get_description().startswith('Store Metadata in a new document')

    def test_meta_update_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataUpdate(app, None)
        assert cmd.get_description().startswith(
            'Update an existing Metadata document by UUID')

    def test_meta_delete_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataDelete(app, None)
        assert cmd.get_description().startswith(
            'Delete a Metadata document by UUID')

    def test_meta_show_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataShow(app, None)
        assert cmd.get_description().startswith(
            'Show a Metadata document by UUID')

    def test_meta_search_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataSearch(app, None)
        assert cmd.get_description().startswith(
            'Search for Metadata documents')

    def test_meta_pems_list_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataPemsList(app, None)
        assert cmd.get_description().startswith(
            'List Permissions for a Metadata document')

    def test_meta_pems_show_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataPemsShow(app, None)
        assert cmd.get_description().startswith(
            'Show Permissions on a Metadata document for specific User')

    def test_meta_pems_grant_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataPemsGrant(app, None)
        assert cmd.get_description().startswith(
            'Grant Permissions on a Metadata document to a User')

    def test_meta_pems_revoke_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataPemsRevoke(app, None)
        assert cmd.get_description().startswith(
            'Revoke Permissions on a Metadata document for a User')

    def test_meta_pems_drop_description(self):
        app = Tapis_App()
        cmd = metadata.MetadataPemsDrop(app, None)
        assert cmd.get_description().startswith(
            'Drop all granted Permissions from a Metadata document')
