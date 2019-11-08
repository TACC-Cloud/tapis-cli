import pytest


@pytest.mark.smoketest
def test_can_import_tapis_cli():
    import tapis_cli


@pytest.mark.smoketest
def test_can_import_actors_modules():
    pass


@pytest.mark.smoketest
def test_can_import_apim_modules():
    from tapis_cli.commands.taccapis.v2.apim import auth_init
    from tapis_cli.commands.taccapis.v2.apim import auth_show
    from tapis_cli.commands.taccapis.v2.apim import token_create
    from tapis_cli.commands.taccapis.v2.apim import token_refresh
    from tapis_cli.commands.taccapis.v2.apim import formatters
    from tapis_cli.commands.taccapis.v2.apim import models


@pytest.mark.smoketest
def test_can_import_apps_modules():
    from tapis_cli.commands.taccapis.v2.apps import create
    from tapis_cli.commands.taccapis.v2.apps import disable
    from tapis_cli.commands.taccapis.v2.apps import enable
    from tapis_cli.commands.taccapis.v2.apps import history
    from tapis_cli.commands.taccapis.v2.apps import list
    from tapis_cli.commands.taccapis.v2.apps import pems_drop
    from tapis_cli.commands.taccapis.v2.apps import pems_grant
    from tapis_cli.commands.taccapis.v2.apps import pems_list
    from tapis_cli.commands.taccapis.v2.apps import pems_revoke
    from tapis_cli.commands.taccapis.v2.apps import publish
    from tapis_cli.commands.taccapis.v2.apps import search
    from tapis_cli.commands.taccapis.v2.apps import show
    from tapis_cli.commands.taccapis.v2.apps import unpublish
    from tapis_cli.commands.taccapis.v2.apps import update
    from tapis_cli.commands.taccapis.v2.apps import formatters
    from tapis_cli.commands.taccapis.v2.apps import models


@pytest.mark.smoketest
def test_can_import_files_modules():
    from tapis_cli.commands.taccapis.v2.files import delete
    from tapis_cli.commands.taccapis.v2.files import download
    from tapis_cli.commands.taccapis.v2.files import history
    from tapis_cli.commands.taccapis.v2.files import list
    from tapis_cli.commands.taccapis.v2.files import pems_drop
    from tapis_cli.commands.taccapis.v2.files import pems_grant
    from tapis_cli.commands.taccapis.v2.files import pems_list
    from tapis_cli.commands.taccapis.v2.files import pems_revoke
    from tapis_cli.commands.taccapis.v2.files import show
    from tapis_cli.commands.taccapis.v2.files import upload
    from tapis_cli.commands.taccapis.v2.files import formatters
    from tapis_cli.commands.taccapis.v2.files import models
    from tapis_cli.commands.taccapis.v2.files import helpers


@pytest.mark.smoketest
def test_can_import_files_helpers():
    from tapis_cli.commands.taccapis.v2.files.helpers.upload import upload
    from tapis_cli.commands.taccapis.v2.files.helpers.sync import download
    from tapis_cli.commands.taccapis.v2.files.helpers.stat import (isfile,
                                                                   isdir, stat,
                                                                   exists)
    from tapis_cli.commands.taccapis.v2.files.helpers.walk import (listdir,
                                                                   walk)
    from tapis_cli.commands.taccapis.v2.files.helpers.pems_list import pems_list


@pytest.mark.smoketest
def test_can_import_jobs_modules():
    from tapis_cli.commands.taccapis.v2.jobs import history
    from tapis_cli.commands.taccapis.v2.jobs import list
    from tapis_cli.commands.taccapis.v2.jobs import outputs_download
    from tapis_cli.commands.taccapis.v2.jobs import outputs_list
    from tapis_cli.commands.taccapis.v2.jobs import resubmit
    from tapis_cli.commands.taccapis.v2.jobs import search
    from tapis_cli.commands.taccapis.v2.jobs import status
    from tapis_cli.commands.taccapis.v2.jobs import submit
    from tapis_cli.commands.taccapis.v2.jobs import formatters
    from tapis_cli.commands.taccapis.v2.jobs import models


@pytest.mark.smoketest
def test_can_import_keys_modules():
    pass


@pytest.mark.smoketest
def test_can_import_metadata_modules():
    from tapis_cli.commands.taccapis.v2.metadata import create
    from tapis_cli.commands.taccapis.v2.metadata import delete
    from tapis_cli.commands.taccapis.v2.metadata import list
    from tapis_cli.commands.taccapis.v2.metadata import search
    from tapis_cli.commands.taccapis.v2.metadata import show
    from tapis_cli.commands.taccapis.v2.metadata import update
    from tapis_cli.commands.taccapis.v2.metadata import formatters
    from tapis_cli.commands.taccapis.v2.metadata import models


@pytest.mark.smoketest
def test_can_import_profiles_modules():
    from tapis_cli.commands.taccapis.v2.profiles import list
    from tapis_cli.commands.taccapis.v2.profiles import show
    from tapis_cli.commands.taccapis.v2.profiles import show_self
    from tapis_cli.commands.taccapis.v2.profiles import formatters
    from tapis_cli.commands.taccapis.v2.profiles import models


@pytest.mark.smoketest
def test_can_import_systems_modules():
    from tapis_cli.commands.taccapis.v2.systems import create
    from tapis_cli.commands.taccapis.v2.systems import disable
    from tapis_cli.commands.taccapis.v2.systems import enable
    from tapis_cli.commands.taccapis.v2.systems import history
    from tapis_cli.commands.taccapis.v2.systems import list
    from tapis_cli.commands.taccapis.v2.systems import publish
    from tapis_cli.commands.taccapis.v2.systems import queues_list
    from tapis_cli.commands.taccapis.v2.systems import roles_drop
    from tapis_cli.commands.taccapis.v2.systems import roles_grant
    from tapis_cli.commands.taccapis.v2.systems import roles_list
    from tapis_cli.commands.taccapis.v2.systems import roles_revoke
    from tapis_cli.commands.taccapis.v2.systems import roles_show
    from tapis_cli.commands.taccapis.v2.systems import search
    from tapis_cli.commands.taccapis.v2.systems import show
    from tapis_cli.commands.taccapis.v2.systems import status
    from tapis_cli.commands.taccapis.v2.systems import unpublish
    from tapis_cli.commands.taccapis.v2.systems import formatters
    from tapis_cli.commands.taccapis.v2.systems import models


@pytest.mark.smoketest
def test_can_import_uuid_modules():
    pass


@pytest.mark.smoketest
def test_can_import_formatone_subclasses():
    from tapis_cli.commands.taccapis.v2.apim.formatters import TokenFormatOne
    from tapis_cli.commands.taccapis.v2.apps.formatters import AppsFormatOne
    from tapis_cli.commands.taccapis.v2.files.formatters import FilesFormatOne
    from tapis_cli.commands.taccapis.v2.jobs.formatters import JobsFormatOne
    from tapis_cli.commands.taccapis.v2.metadata.formatters import MetadataFormatOne
    from tapis_cli.commands.taccapis.v2.profiles.formatters import ProfilesFormatOne
    from tapis_cli.commands.taccapis.v2.systems.formatters import SystemsFormatOne


@pytest.mark.smoketest
def test_can_import_formatmany_subclasses():
    from tapis_cli.commands.taccapis.v2.apps.formatters import AppsFormatMany
    from tapis_cli.commands.taccapis.v2.files.formatters import FilesFormatMany
    from tapis_cli.commands.taccapis.v2.jobs.formatters import JobsFormatMany
    from tapis_cli.commands.taccapis.v2.metadata.formatters import MetadataFormatMany
    from tapis_cli.commands.taccapis.v2.profiles.formatters import ProfilesFormatMany
    from tapis_cli.commands.taccapis.v2.systems.formatters import SystemsFormatMany


@pytest.mark.smoketest
@pytest.mark.parametrize('attribute,accept_none,expect_exception',
                         [('title', False, False), ('url', False, True)])
def test_about(attribute, accept_none, expect_exception):
    from tapis_cli import About

    def test_code():
        a = About()
        val = getattr(a, attribute)
        if val is None and not accept_none:
            raise ValueError('{} cannot be None'.format(attribute))
