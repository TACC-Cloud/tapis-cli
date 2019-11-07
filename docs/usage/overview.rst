Overview
========

Tapis CLI implements a consistent grammar and syntax for all Tapis services,
as well as for client-side workflows (such as application publishing) that
coordinate multiple API calls across different services. Verbs are named
consistently across services, as are subjects and objects. Usually, entity
names and verbs track perfectly to the underlying API, but in some cases,
revisions have been made for clarity based on user feedback.

The top-level command is **tapis** and has the following usage options.

.. code-block:: shell

    $ tapis -h
    usage: tapis [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

    Tapis CLI: Command line tools to support the TACC Tapis platform. For support
    contact "TACC Help" <cli-help@tacc.cloud>

    optional arguments:
    --version            show program's version number and exit
    -v, --verbose        Increase verbosity of output. Can be repeated.
    -q, --quiet          Suppress output except warnings and errors.
    --log-file LOG_FILE  Specify a file to log output. Disabled by default.
    -h, --help           Show help message and exit.
    --debug              Show tracebacks on errors.

Verbose
-------

The ``-v`` flag replicates and extends the original Bash CLI feature of
presenting the results from an API command as JSON. Please note that while
every attempt is made to avoid any changes, the displayed JSON is rendered
by the CLI rather than being displayed directly as it comes back from the
service. This was critical for implementing robust error handling.

Help
----

Every command and subcommand has a help option. It is accessible by passing
``-h``. Please use this as much effort has gone into making the help text
consistent and correct across the entire CLI.

Debug
-----

Inevitably, an error will be encountered. The **cliff** framework that the
CLI is implemented in does a great job at swallowing errors, printing out
just a summary to the screen when they occur. To see a detailed Python
stack trace (for example, if you are trying to file an issue), repeat the
failed command with the ``--debug`` flag set.

