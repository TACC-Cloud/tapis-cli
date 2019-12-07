Installing Tapis CLI
====================

Tapis CLI is available as a Python package. You can visit its GitHub repository
or get the latest version from PyPI: ``pip install tapis-cli``

We highly recommend using Python 3.7+ as the Python runtime behind Tapis CLI.
We support Python 2.7 for legacy applications, but on a best-effort basis as
Python 2.7 is a deprecated language.

From Source
-----------

.. code-block:: shell

    $ git clone https://github.com/TACC-Cloud/tapis-cli-ng.git
    $ cd tapis-cli-ng
    $ pip install --upgrade --user .

Container Image
---------------

As an alternative to local installation, the CLI is available as a public
DockerHub_ image ``tacc/tapis-cli-ng:latest``. Run it like so:

.. code-block:: shell

    docker run --rm -it -v ${PWD}:/work -v ${HOME}/.agave:/root/.agave \
        tacc/tapis-cli-ng:latest bash

.. _DockerHub: https://hub.docker.com/r/tacc/tapis-cli-ng
