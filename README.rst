Tapis CLI
=========

Install
-------

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
