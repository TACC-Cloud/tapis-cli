Tapis CLI
=========

.. warning::

   The authentication subsystem is not yet implemented (9/4/2019). You will need to use the ``auth-tokens-*`` tools bundled with the Bash Tapis CLI to create and refresh Oauth2 access tokens.

Installation
------------

.. code-block:: shell

    $ git clone https://github.com/TACC-Cloud/tapis_cli_ng.git
    $ cd tapis_cli_ng
    $ pip install --user -e .

Getting Started
---------------

The CLI features extensive contextual help, which should help you learn to use
it. To start, a listing of supported commands and global options can be \
shown with ``--help``:

.. code-block:: shell

    $ tapis --help

There is also a ``help`` command for any for specific command:

.. code-block:: shell

    $ tapis help versions
    $ tapis versions --help

Example
^^^^^^^

The following illustrates use of one of the **search** commands to find apps
named *word-count*. The equality operator **eq** will constrain the results to
exact matches. Other operators include **neq** and **like**.

.. code-block:: shell

    $ tapis apps search --name eq "word-count"

    +---------------+----------+------------+---------------+------------------+----------+-----------------+
    | id            | revision | label      | lastModified  | shortDescription | isPublic | executionSystem |
    +---------------+----------+------------+---------------+------------------+----------+-----------------+
    | word-         |       29 | Word Count | 2019-08-31T06 | How many words   | False    | hpc-tacc-       |
    | count-0.1     |          |            | :21:20.000-05 | are in a file?   |          | jetstream       |
    |               |          |            | :00           | Guess randomly   |          |                 |
    |               |          |            |               | or use ADVanCEd  |          |                 |
    |               |          |            |               | aNalYTIcaL       |          |                 |
    |               |          |            |               | tECHnIqUES to    |          |                 |
    |               |          |            |               | figure it out.   |          |                 |
    | word-         |        1 | Word Count | 2019-02-21T17 | How many words   | True     | hpc-tacc-       |
    | count-0.1u1   |          |            | :56:14.000-06 | are in a file?   |          | maverick        |
    |               |          |            | :00           | Guess randomly   |          |                 |
    |               |          |            |               | or use ADVanCEd  |          |                 |
    |               |          |            |               | aNalYTIcaL       |          |                 |
    |               |          |            |               | tECHnIqUES to    |          |                 |
    |               |          |            |               | figure it out.   |          |                 |
    +---------------+----------+------------+---------------+------------------+----------+-----------------+

Get details for one specific record using a **show** command, like so:

.. code-block:: shell

    $ tapis apps show word-count-0.1u1

    +--------------------------+-------------------------------+
    | Field                    | Value                         |
    +--------------------------+-------------------------------+
    | id                       | word-count-0.1u1              |
    | name                     | word-count                    |
    | version                  | 0.1                           |
    | revision                 | 1                             |
    | label                    | Word Count                    |
    | lastModified             | 7 months ago                  |
    | shortDescription         | How many words are in a file? |
    |                          | Guess randomly or use         |
    |                          | ADVanCEd aNalYTIcaL           |
    |                          | tECHnIqUES to figure it out.  |
    | longDescription          | Counts words in a file        |
    | owner                    | sd2eadm                       |
    | isPublic                 | True                          |
    | executionType            | HPC                           |
    | executionSystem          | hpc-tacc-maverick             |
    | deploymentSystem         | data-sd2e-projects-users      |
    | available                | True                          |
    | parallelism              | SERIAL                        |
    | defaultProcessorsPerNode | 1                             |
    | defaultMemoryPerNode     | 1                             |
    | defaultNodeCount         | 1                             |
    | defaultMaxRunTime        | 00:05:00                      |
    | defaultQueue             | None                          |
    | helpURI                  | https://sd2e.org/develop/     |
    | deploymentPath           | /.public-apps/word-           |
    |                          | count-0.1u1.zip               |
    | templatePath             | runner-template.sh            |
    | testPath                 | tester.sh                     |
    | checkpointable           | False                         |
    | uuid                     | 4975805169073918441-242ac11a- |
    |                          | 0001-005                      |
    | icon                     | None                          |
    +--------------------------+-------------------------------+

Get the JSON representation for the record by passing the **verbose** flag:

.. code-block:: shell

    $ tapis apps show word-count-0.1u1 -v


Shell completion
^^^^^^^^^^^^^^^^

One may install bash command line completion to get command hints by tabbing.

.. code-block:: shell

    $ tapis complete >> ~/.bash_aliases
    $ . ~/.bash_aliases  # add to ~/.bashrc or ~/.bash_profile to always load (Ubuntu distros already load it)
    $ tapis <tab>
        complete     help         statuses     versions

.. note::

    **Mac OS X Users**: One may need to install autocomplete support before
    this works. Using Homebrew, do ``brew install bash-completion``.

Configuration
-------------

The Tapis CLI uses Python's ``dotenv`` module for configuration via environment
variables. Briefly, the CLI will look for a file ``.env`` containing
``KEY=VALUE`` pairs starting in the current working directory and working up
the parent directory tree. If it still cannot find an environment file, it
looks in ``$HOME/.env`` for one. Any variable defined in the environment
file can be overridden by setting an environment variable in the shell where
the CLI was launched. Some options can be further overridden at run-time via
command-line option.

Example
^^^^^^^

The number of results returned from list-type commands is defined by the
variable ``PAGE_SIZE`` and defaults to **100**. All CLI list-type commands
support a ``--pagesize`` option, which will be used if specified. If no option
is passed, the CLI will look for variable ``PAGE_SIZE`` first in the shell
environment, then in a ``.env`` file.

Briefly restated::

    --pagesize > os.environ['PAGE_SIZE'] > ./.env > $HOME.env

The Settings Command
^^^^^^^^^^^^^^^^^^^^

One may view the current settings for the Tapis CLI as documented below. It is
not yet possible to  edit settings in the CLI directly.

.. code-block:: shell

    $ tapis settings list
    +-----------------------------+-------------------------------------+
    | Setting                     | Value                               |
    +-----------------------------+-------------------------------------+
    | ENV_PREFIX                  | TAPIS_CLI                           |
    | DEBUG_MODE                  | False                               |
    | DATE_FORMAT                 | YYYYMMDDTHHmmssZZ                   |
    | LOG_LEVEL                   | INFO                                |
    | PAGE_SIZE                   | 30                                  |
    | RESPONSE_FORMAT             | None                                |
    | FIT_WIDTH                   | True                                |
    | TENANT_DNS_DOMAIN           | tacc.utexas.edu                     |
    | TACC_PROJECT_NAME           | TAPIS_SANDBOX                       |
    | TACC_PROJECT_ID             | 65536                               |
    | TACC_TENANT_ID              | tacc.prod                           |
    | TACC_PROJECT_GROUP          | 131072                              |
    | TACC_MANAGER_ACCOUNT        | tacolord                            |
    | TACC_TENANTS_SERVER         | https://api.tacc.utexas.edu/tenants |
    | TACC_API_SERVER             | https://api.tacc.utexas.edu/        |
    | TACC_JUPYTER_SERVER         | https://jupyter.tacc.utexas.edu     |
    | TACC_PRIMARY_STORAGE_SYSTEM | data-tapis-sandbox                  |
    | TACC_GITLAB_SERVER          | git.tacc.utexas.edu                 |
    | TACC_GITLAB_URI             | https://git.tacc.utexas.edu         |
    +-----------------------------+-------------------------------------+

Hacking
-------

Install CLI in editable mode::

    pip install -e .

Run all the tests::

    python -m pytest

Run tests with tox::

    pip install tox
    tox

Documentation
-------------

The project uses Sphinx plus the Napoleon extension, which is configured to
support Google-style documentation strings.

Regenerate the documentation::

    make docs

Contributing
------------

The project code style is vanilla PEP8, as configured by the
``[flake8]`` section of ``setup.cfg``. Use of ``yapf`` autoformatter is
supported and encouraged to maintain the codebase, and is available via the
``make format`` Makefile target.
