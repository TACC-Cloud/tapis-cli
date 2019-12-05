Configure Tapis CLI
-------------------

The Tapis CLI uses Python's ``dotenv`` module for configuration via environment
variables. Briefly, the CLI will look for a file ``.env`` containing
``KEY=VALUE`` pairs starting in the current working directory and working up
the parent directory tree. If it still cannot find an environment file, it
looks in ``$HOME/.env`` for one. Any variable defined in the environment
file can be overridden by setting an environment variable in the shell where
the CLI was launched. Some options can be further overridden at run-time via
command-line option.

One may view the current settings for the Tapis CLI:

.. code-block:: shell

    $ tapis config list
    +---------------------------+--------------------------------------------+
    | Setting                   | Value                                      |
    +---------------------------+--------------------------------------------+
    | TAPIS_CLI_DATE_FORMAT     | YYYYMMDDTHHmmssZZ                          |
    | TAPIS_CLI_DEBUG_MODE      | False                                      |
    | TAPIS_CLI_DISPLAY_AUP     | True                                       |
    | TAPIS_CLI_FIT_WIDTH       | True                                       |
    | TAPIS_CLI_GA_DISABLE      | False                                      |
    | TAPIS_CLI_GA_VISITOR      | 7143393360                                 |
    | TAPIS_CLI_LOG_LEVEL       | DEBUG                                      |
    | TAPIS_CLI_PAGE_SIZE       | 50                                         |
    | TAPIS_CLI_RESPONSE_FORMAT | table                                      |
    | TAPIS_CLI_SHOW_CURL       | False                                      |
    | TAPIS_CLI_VERBOSE_ERRORS  | True                                       |
    | TAPIS_DEFAULT_TENANT_ID   | tacc.prod                                  |
    | TAPIS_PY_SHOW_CURL        | False                                      |
    | TAPIS_TENANTS_URL         | https://api.tacc.utexas.edu/tenants        |
    | _ENV_PATH                 | /Users/tacotruck/.env                      |
    +---------------------------+--------------------------------------------+

Configuration options can be set using ``tapis config set``.

An Example
----------

The number of results returned from list-type commands is defined by the
variable ``TAPIS_CLI_PAGE_SIZE`` and defaults to **50**. List-type commands
support a ``--limit`` option, which will be used if specified. If no option
is passed, the CLI will look for variable ``TAPIS_CLI_PAGE_SIZE`` in the shell
environment then in a ``.env`` file. Here are ways to configure the page size:

    - Dynamically, via argument: ``tapis apps list --limit 10``
    - Dynamically, via variable: ``TAPIS_CLI_PAGE_SIZE=10 tapis apps list``
    - For the current shell: ``export TAPIS_CLI_PAGE_SIZE=10``
    - For all future usage: ``tapis apps set TAPIS_CLI_PAGE_SIZE 10``

Key Settings
------------

**Coming soon**

