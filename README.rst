Tapis CLI
=========

|build-status| |docs| |doi|

Tapis CLI is a human-friendly, scriptable command line interface, implemented in
Python, that helps scientists and engineers build and manage scalable computational
and data science workflow projects using TACC's Tapis platform. It is a
replacement for a pure-Bash CLI environment known as agave-cli that we hope
brings you new features, better reliability, and dramatically enhanced
productivity.

Tapis CLI provides a unified interface to multiple platform APIs, allowing them
to be easily orchestrated and composed into higher-order constructs combining
HPC, data management, cloud computing, and other aspects of computing.

Installation
------------

.. code-block:: shell

    $ git clone https://github.com/TACC-Cloud/tapis-cli-ng.git
    $ cd tapis-cli-ng
    $ pip install --upgrade --user .

Docker Container Image
^^^^^^^^^^^^^^^^^^^^^^

As an alternative to local installation, the CLI is available as a public
Docker image ``tacc/tapis-cli-ng:latest``. Run it like so:

.. code-block:: shell

    docker run --rm -it -v ${PWD}:/work -v ${HOME}/.agave:/root/.agave \
        tacc/tapis-cli-ng:latest bash

Initialize a Session
--------------------

You must set up a Tapis session on each host where you will use Tapis CLI. This
is a scripted process implemented by ``tapis auth init``. Here's an example:

.. code-block:: shell

    $ tapis auth init

    Use of Tapis requires acceptance of the TACC Acceptable Use Policy,
    which can be found at https://portal.tacc.utexas.edu/tacc-usage-policy

    Do you agree to abide by the AUP? (type 'y' or 'n' then Return) y

    To improve our ability to support Tapis and the Tapis CLI, we would like to
    collect your IP addrress, operating system and Python version. No personally-
    identifiable information will be collected. This data will only be shared in
    aggregate form with funders and Tapis platform stakeholders.

    Do you consent to this reporting? [Y/n]: y

    Available Tenants
    =================
    3dem	agave.prod	araport.org	bridge	designsafe
    iplantc.org	irec	portals	sd2e	sgci
    tacc.prod	vdjserver.org

    Enter a tenant name: tacc.prod
    Username: tacotron
    Password for tacotron:
    +--------------+---------------------------------+
    | Field        | Value                           |
    +--------------+---------------------------------+
    | tenant_id    | tacc.prod                       |
    | username     | tacotron                        |
    | client_name  | _cli-tacc.prod-tacotron-macbook |
    | api_key      | uAShaDfy0vF7hgFcAqx7oeAtO6oa    |
    | access_token | a31c66cfaa45451c95df6fd473ffd4b |
    | expires_at   | Thu Sep 19 14:08:37 2019        |
    +--------------+---------------------------------+

Getting Started
---------------

The CLI features extensive contextual help. To start, one may get a listing of
supported commands and global options via  ``--help``.

.. code-block:: shell

    $ tapis --help

Find available subcommands:

.. code-block:: shell

    $ tapis apps --help
    Command "apps" matches:
    apps create
    apps disable
    apps enable
    apps history
    apps list
    apps pems grant
    apps pems list
    apps pems revoke
    apps pems show
    apps publish
    apps search
    apps show
    apps unpublish
    apps update

Get Help:

.. code-block:: shell

    $ tapis --help

There is a ``--help`` flag for each command.

.. code-block:: shell

    $ tapis help apps list
    $ # or
    $ tapis apps list --help

Hacking
-------

Install CLI in editable mode::

    pip install -e .

Run all the tests::

    python -m pytest

Run tests with tox::

    # Note tox is not included in requirements.txt
    pip install tox
    tox

Code structure
--------------

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

Documentation
-------------

The project uses Sphinx and the Napoleon extension, which is configured to
support Google-style documentation strings.

Regenerate the documentation::

    make docs

Code Style
----------

The project code style is vanilla PEP8, as configured by the
``[flake8]`` section of ``setup.cfg``. Use of ``yapf`` autoformatter is
supported and encouraged to maintain the codebase, and is available via the
``make format`` Makefile target.

Roadmap and Issue Tracker
-------------------------

Major functional objectives are bundled into Milestones_ with due dates in the
future. This provides a way to organize the work and have a public road map
for functionality.

All work should proceed through at least one or more reported Issues_.

.. _Milestones: https://github.com/TACC-Cloud/tapis-cli-ng/milestones?direction=asc&sort=due_date&state=open
.. _Issues: https://github.com/TACC-Cloud/tapis-cli-ng/issues


.. |build-status| image:: https://travis-ci.org/TACC-Cloud/tapis-cli-ng.svg?branch=master&style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/TACC-Cloud/tapis-cli-ng

.. |docs| image:: https://readthedocs.org/projects/tapis-cli/badge/?version=latest
    :alt: Documentation
    :scale: 100%
    :target: https://tapis-cli.readthedocs.io/

.. |doi| image:: https://zenodo.org/badge/203083094.svg
    :alt: Publication
    :scale: 100%
    :target: https://zenodo.org/badge/latestdoi/203083094
