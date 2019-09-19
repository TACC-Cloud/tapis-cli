Tapis CLI
=========

Installation
------------

.. code-block:: shell

    $ git clone https://github.com/TACC-Cloud/tapis_cli_ng.git
    $ cd tapis_cli_ng
    $ pip install --user .

Docker Container Image
^^^^^^^^^^^^^^^^^^^^^^

As an alternative to local installation, the CLI is available as a public
Docker image ``tacc/tapis-cli-ng:latest``. Run it like so:

.. code-block:: shell

    docker run --rm -it -v ${PWD}:/work -v ${HOME}/.agave:/root/.agave \
        tacc/tapis-cli-ng:latest bash

A local build of the image can be created and launched using ``make image``
followed by ``make interactive``.

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
---------------------------

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
tenant/username combination. Explicitly switching between profiles
(``tapis auth switch``) is not currently supported.

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
presented as command line options. Search modifiers are supported.

This is an example of what the help looks like for a search command.

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

This help tells you that any named field (**id**, **parallelism**, **owner**,
etc.) can be searched.

The following illustrates a simple search for an app with a specific name. The
equality (**eq**) will constrain the result to identical matches, while
**like** would allow the search term to a substring.


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

Drill down into the details for a specific application using a show command.

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
------

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
^^^^^^^^^^^^^^

API commands are implemented as clients implemented in the ``clients``
submodule. There are essentially two kinds of clients: A ``Lister`` and
a ``ShowOne`` client, where the lister handles multiple responses and single
records are handled by ``ShowOne``. Clients can be extended through the use of
classes defined in ``clients.services.mixins``

Each new command is implemented in a TitleCased class in a snake_case
submodule organized by platform and service under ``commands``. For instance,
the ``apps list`` command is defined by ``tapis_cli.commands.taccapis.v2.apps:AppsList``.

The CLI uses setuptools entrypoints to establish command line functions
available in a user's shell. See the ``[entry_points]`` section of ``setup.cfg``
for details. Note the location of ``tapis_cli.commands.taccapis.v2.apps:AppsList`` in
this document.

Very limited unit tests are implemented in the `tests` directory. Linting and
code coverage are included in the automated test process.

Documentation
^^^^^^^^^^^^^

The project uses Sphinx plus the Napoleon extension, which is configured to
support Google-style documentation strings.

Regenerate the documentation::

    make docs

Code Style
^^^^^^^^^^

The project code style is vanilla PEP8, as configured by the
``[flake8]`` section of ``setup.cfg``. Use of ``yapf`` autoformatter is
supported and encouraged to maintain the codebase, and is available via the
``make format`` Makefile target.

Issue Management
^^^^^^^^^^^^^^^^

Please file and track issues on the project issues page.
