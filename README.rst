Tapis CLI
=========

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

(Optional) One may install bash command line completion to get command hints
by tabbing.

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

Development
-----------

Install developer dependencies::

    pip install -r requirements-dev.txt

Run all the tests::

    python -m pytest

Documentation
-------------

The project uses Sphinx plus the Napoleon extension, which is configured to
support Google-style documentation strings.

Regenerate the documentation::

    make docs

Contributing
------------

The project code style is pretty vanilla PEP8, as configured by the
``[flake8]`` section of ``setup.cfg``. Use of ``yapf`` autoformatter is
supported and encouraged to maintain the codebase, and is available via the
``make format`` Makefile target.
