Tapis CLI
=========

.. image:: https://travis-ci.org/TACC-Cloud/tapis-cli-ng.svg?branch=master
    :target: https://travis-ci.org/TACC-Cloud/tapis-cli-ng

.. image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://raw.githubusercontent.com/TACC-Cloud/tapis-cli-ng/master/LICENSE.txt

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

A local build of the image can be created and launched using ``make image``
followed by ``make interactive``. Previous builds are available on
[Docker Hub](https://hub.docker.com/r/tacc/tapis-cli-ng).

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

Initializing a Tapis Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This release marks the debut of a simplified scheme in which a single
host-specific client is generated and maintained for each combination of
tenant and username. To initialize a host to use Tapis, simply run
``tapis auth init`` command.

.. code-block:: shell

    $ tapis auth init
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

Re-running without changing tenant or username will display the current auth
context, while changing either tenant or username (or specifying
``--interactive`` mode) will re-initialize the host to use the specified
tenant/username combination.

Explicit configuration switching (``tapis auth switch``) is not (yet) supported.

**NOTE** If you have a configured, but expired Agave client in
``~/.agave/current``, the ``init`` command may fail to detect the expiration
and may skip a key step. If you get a message ``Tapis client appears invalid``
re-run with ``tapis auth init --interactive`` and follow the prompts.

Usage Examples
--------------

The following illustrate basic patterns implemented in each Tapis CLI command.
Explore their help documents to learn more details.

List
^^^^

Simply list resources (apps, in this case) known to an API. List commands
support **limit** and **offset** arguments.

.. code-block:: shell

    $ tapis apps list --limit 3
    +-------------------------------+------------------+
    | id                            | label            |
    +-------------------------------+------------------+
    | tapis.app.imageclassify-1.0u1 | Image Classifier |
    | vina-ls5-1.1.2u3              | Autodock Vina    |
    | vina-ls5-1.1.2u2              | Autodock Vina    |
    +-------------------------------+------------------+

Search
^^^^^^

It is possible to search for resources matching specific fields. Rather than
require a user to remember complicated query syntax, searchable fields are
presented as command line options. Search modifiers are supported. Search
commands also support **limit** and **offset** arguments.

This is an example of help for a search command.

.. code-block:: shell

    $ tapis apps search -h
    usage: tapis apps search [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                            [--quote {all,minimal,none,nonnumeric}] [--noindent]
                            [--max-width <integer>] [--fit-width] [--print-empty]
                            [--sort-column SORT_COLUMN] [--no-verify]
                            [-H API_SERVER] [-z ACCESS_TOKEN] [-l LIMIT]
                            [-o OFFSET] [--id mod STRING] [--name mod STRING]
                            [--version mod STRING] [--revision mod INT]
                            [--label mod STRING] [--short-description mod STRING]
                            [--long-description mod STRING] [--owner mod STRING]
                            [--public mod TRUE] [--execution-type mod STRING]
                            [--execution-system mod STRING]
                            [--deployment-system mod STRING]
                            [--available mod TRUE] [--parallelism mod STRING]
                            [--default-processors-per-node mod INT]
                            [--default-memory-per-node mod INT]
                            [--default-node-count mod INT]
                            [--default-max-run-time mod STRING]
                            [--default-queue mod STRING]

    Search the Apps catalog

    optional arguments:
    -h, --help            show this help message and exit
    --no-verify           Allow insecure server connections when using SSL
    -H API_SERVER, --api-server API_SERVER
                            Tapis API server
    -z ACCESS_TOKEN, --token ACCESS_TOKEN
                            Tapis access_token
    -l LIMIT, --limit LIMIT
                            Limit to L records
    -o OFFSET, --offset OFFSET
                            Skip first O records

    Search arguments:
    --id mod STRING
    --name mod STRING
    --version mod STRING
    --revision mod INT
    --label mod STRING
    --short-description mod STRING
    --long-description mod STRING
    --owner mod STRING
    --public mod TRUE
    --execution-type mod STRING
    --execution-system mod STRING
    --deployment-system mod STRING
    --available mod TRUE
    --parallelism mod STRING
    --default-processors-per-node mod INT
    --default-memory-per-node mod INT
    --default-node-count mod INT
    --default-max-run-time mod STRING
    --default-queue mod STRING

Any named field (**id**, **parallelism**, **owner**, etc.) can be searched.
Here is an illustration of searching for an app by specific **name**. The
equality (**eq**) modifier constrains the result to identical matches. Using
**like** allows the search term to a match a substring. Wildcards or
regular expressions are not (currently) supported.

.. code-block:: shell

    $ tapis apps search --name eq vina-ls5
    +------------------+----------+---------------+--------------------+--------+------------------+
    | id               | revision | label         | shortDescription   | public | executionSystem  |
    +------------------+----------+---------------+--------------------+--------+------------------+
    | vina-ls5-1.1.2u3 |        3 | Autodock Vina | AutoDock Vina is   | None   | docking.exec.ls5 |
    |                  |          |               | an open-source     |        |                  |
    |                  |          |               | program for doing  |        |                  |
    |                  |          |               | molecular docking  |        |                  |
    | vina-ls5-1.1.2u2 |        2 | Autodock Vina | AutoDock Vina is   | None   | docking.exec.ls5 |
    |                  |          |               | an open-source     |        |                  |
    |                  |          |               | program for doing  |        |                  |
    |                  |          |               | molecular docking  |        |                  |
    | vina-ls5-1.1.2u1 |        1 | Autodock Vina | AutoDock Vina is   | None   | docking.exec.ls5 |
    |                  |          |               | an open-source     |        |                  |
    |                  |          |               | program for doing  |        |                  |
    |                  |          |               | molecular docking  |        |                  |
    +------------------+----------+---------------+--------------------+--------+------------------+
    $ tapis apps search --name eq image
    (None)
    $ tapis apps search --name like image
    +------------------+----------+------------------+------------------+--------+---------------------+
    | id               | revision | label            | shortDescription | public | executionSystem     |
    +------------------+----------+------------------+------------------+--------+---------------------+
    | tapis.app.imagec |        3 | Image Classifier | Classify an      | None   | tapis.execution.sys |
    | lassify-1.0u3    |          |                  | image using a    |        | tem                 |
    |                  |          |                  | small ImageNet   |        |                     |
    |                  |          |                  | model            |        |                     |
    | tapis.app.imagec |        2 | Image Classifier | Classify an      | None   | tapis.execution.sys |
    | lassify-1.0u2    |          |                  | image using a    |        | tem                 |
    |                  |          |                  | small ImageNet   |        |                     |
    |                  |          |                  | model            |        |                     |
    | tapis.app.imagec |        1 | Image Classifier | Classify an      | None   | tapis.execution.sys |
    | lassify-1.0u1    |          |                  | image using a    |        | tem                 |
    |                  |          |                  | small ImageNet   |        |                     |
    |                  |          |                  | model            |        |                     |
    +------------------+----------+------------------+------------------+--------+---------------------+

Show
^^^^

A show command replicates the original CLI behavior where
``<service>> list <<identifier>>`` would return a detailed display of one
specific Tapis entity. The new CLI separates this out into its own verb for
the sake of clarity.

.. code-block:: shell

    $ tapis apps show tapis.app.imageclassify-1.0u3
    +--------------------------+------------------------------------------------------------------+
    | Field                    | Value                                                            |
    +--------------------------+------------------------------------------------------------------+
    | id                       | tapis.app.imageclassify-1.0u3                                    |
    | name                     | tapis.app.imageclassify                                          |
    | version                  | 1.0                                                              |
    | revision                 | 3                                                                |
    | label                    | Image Classifier                                                 |
    | lastModified             | 6 days ago                                                       |
    | shortDescription         | Classify an image using a small ImageNet model                   |
    | longDescription          |                                                                  |
    | owner                    | cicsvc                                                           |
    | public                   | None                                                             |
    | executionType            | CLI                                                              |
    | executionSystem          | tapis.execution.system                                           |
    | deploymentSystem         | docking.storage                                                  |
    | available                | True                                                             |
    | parallelism              | SERIAL                                                           |
    | defaultProcessorsPerNode | 1                                                                |
    | defaultMemoryPerNode     | 1                                                                |
    | defaultNodeCount         | 1                                                                |
    | defaultMaxRunTime        | None                                                             |
    | defaultQueue             | None                                                             |
    | helpURI                  |                                                                  |
    | deploymentPath           | /home/docking/api/v2/prod/apps/tapis.app.imageclassify-1.0u3.zip |
    | templatePath             | wrapper.sh                                                       |
    | testPath                 | test/test.sh                                                     |
    | checkpointable           | False                                                            |
    | uuid                     | 3162334876895875561-242ac119-0001-005                            |
    | icon                     | None                                                             |
    +--------------------------+------------------------------------------------------------------+

One can get a JSON representation of the record by passing the **verbose** flag:

.. code-block:: shell

    $ tapis apps show tapis.app.imageclassify-1.0u3 -v

Update
^^^^^^

Assume one is the author (or an authorized contributor) to
**tapis.app.imageclassify**: The Tapis metadata for the app can be updated
usng ``tapis apps update <app_id>``. Here's an example:

.. code-block:: shell

    $ tapis apps update -F imageclassif.json tapis.app.imageclassify-1.0

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

This combination of mixture of code namespacing and configuration is intended
to support migration of specific services to new versions, while maintaining
code and capability to support earlier versions.

Commands are further constructed using mix-in classes. These are all (for now)
defined in ``tapis_cli.clients.services.mixins``. Examples include a class
``ServiceIdentifier`` which makes a command require an identifier to be
specified as a positional parameter, and ``JsonVerbose`` which extends cliff's
``-v`` flag to automatically turn up the number of fields reported to the
maximum allowed by the command and to force a switch to the JSON formatter.

Within the service-level package for each command is a ``models`` sub-package
where the "data model (or models)" for the service are defined. In **apps**,
one has ``App``, ``AppPermission``, and ``AppHistory``.

Model classes aren't really models in the strict sense of the word, as they
don't encode any knowledge of how the underlying API code works. Instead, their
primary role is to define the top-level fields returned by each service, in
what context the field is returned, and whether the field is searchable.
They also encode rules for how to render specific fields for display. For
example, there is a rule defined in the ``File`` model to humanize display of
file sizes when the display formatter is anything but JSON, and another one
to transform "Agave" style permissions (``READ_WRITE``) to be better aligned
with the UNIX shell environment (``rw-``).

Very limited unit tests are implemented in the `tests` directory, which make
extensive use of fixtures to minimize duplication of text code.

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
