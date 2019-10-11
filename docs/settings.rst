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
    | TENANT_GITLAB_SERVER          | git.tacc.utexas.edu                 |
    | TENANT_GITLAB_URL             | https://git.tacc.utexas.edu         |
    +-----------------------------+-------------------------------------+
