#########################
Contributing to Tapis CLI
#########################

We welcome contributions to Tapis CLI, since our users are often best qualified
to propose and improve its functionality.

*******
Hacking
*******

Install CLI in editable mode::

    pip install -e .

Run all the tests::

    python -m pytest

Run multi-environment tests with tox::

    # Note tox is not included in requirements.txt
    pip install tox
    tox

************
Docker image
************

A local build of the Tapis CLI container image can be created and launched
using ``make image`` followed by ``make interactive``. This is helpful when
customizing or extending the project Dockerfile.

**************
Code structure
**************

API commands are implemented as subclasses of ``TaccApisCommandBase``, which
handles Oauth client setup, and either ``TaccApisFormatOne`` or
``TaccApisFormatMany``, which are in turn subclassed from cliff's ``Lister``
and ``FormatMany`` classes. This design reflects two kinds of responses: a
list of records or a single record (or response to a CRUD action).

Each command is implemented as a TitleCased class in a snake_cased module,
which in turn are organized by platform, version, and service under the
``commands`` subpackage. Consider the ``tapis apps list`` command. It is one
of the Tapis APIs, the command being implemented is specific to the **v2**
version of TACC APIs, and is a command pertaining to the **apps** service.
Thus, the command is defined in class ``AppsList`` in
``tapis_cli.commands.taccapis.v2.apps.apps_list``.

This code structure reflects two requirements. The first is that the cliff
package uses setuptools entrypoints to establish command line functions. The
second is that the Tapis CLI will integrate multiple platforms and versions of
TACC-hosted services. There is space marked out in the CLI design for **v3**
of Tapis, management functions for hosted Gitlab and Container registry, and
eventual public release of the TACC SSH Keys service.

Returning to the setuptools topic: Each command is defined in ``setup.cfg``
by defining a command and pointing to the implementing class. The ``apps list``
command is defined as shown below.

Example setuptools entrypoint::

    [entry_points]
    console_scripts =
        tapis = tapis_cli.main:main
    tapis.cli =
        apps_list = tapis_cli.commands.taccapis.v2.apps:AppsList

Limited (at present) unit tests are implemented in the `tests` directory.
Automated code linting (to PEP8) and code coverage analysis are included in
all PyTest runs to encourage sustainable development practices.

*************
Documentation
*************

The project uses Sphinx and the Napoleon extension, which is configured to
support Google-style documentation strings.

Regenerate the documentation::

    make docs

**********
Code Style
**********

The project code style is vanilla PEP8, as configured by the
``[flake8]`` section of ``setup.cfg``. 

Use of ``yapf`` autoformatter is supported and encouraged to 
maintain the codebase, and is available via the ``make format`` 
Makefile target.

*************
Issue Tracker
*************

Major functional objectives are bundled into Milestones_ with due dates in the
future. This provides a way to organize the work and have a public road map
for functionality.

All work should proceed via reported Issues_.

.. _Milestones: https://github.com/TACC-Cloud/tapis-cli-ng/milestones?direction=asc&sort=due_date&state=open
.. _Issues: https://github.com/TACC-Cloud/tapis-cli-ng/issues

