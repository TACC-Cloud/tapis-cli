###################
Configure Tapis CLI
###################

The Tapis CLI uses Python's _dotenv module for configuration via environment
variables. It reads and writes from ``$HOME/.env``, which is a file containing 
``KEY=VALUE`` pairs. A variable defined in the environment file can be 
overridden by setting an environment variable in the shell where the CLI 
was launched. Some options can also overridden at run-time via
command-line options.

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

**************
Usage Examples
**************

**Setting the page size for list results**: The number of results returned from 
list-type commands is defined by the variable ``TAPIS_CLI_PAGE_SIZE`` and 
defaults to **50**. List-type commands support a ``--limit`` option, which 
will be used if specified. If no option is passed, the CLI will look for 
variable ``TAPIS_CLI_PAGE_SIZE`` in the shell environment then in an
 ``.env`` file. Here are ways to configure the page size:

    - Dynamically, via variable: ``TAPIS_CLI_PAGE_SIZE=10 tapis apps list``
    - For the current shell: ``export TAPIS_CLI_PAGE_SIZE=10``
    - For all future usage: ``tapis apps set TAPIS_CLI_PAGE_SIZE 10``

