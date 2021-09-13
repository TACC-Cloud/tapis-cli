#########
Tapis CLI
#########

|build-status| |docs| |doi|

Tapis CLI is a human-friendly, scriptable command line interface, implemented in
Python, that helps scientists and engineers build and manage scalable computational
and data science workflow projects using the Tapis_ platform. It is a
replacement for a pure-Bash CLI environment known as agave-cli that we hope
brings you new features, better reliability, and dramatically enhanced
productivity.

Tapis CLI provides a unified interface to multiple web service APIs, allowing them
to be easily orchestrated and composed into higher-order constructs combining
HPC, data management, cloud computing, and other aspects of computing.

Documentation: `https://tapis-cli.readthedocs.io/en/latest/ <https://tapis-cli.readthedocs.io/en/latest/>`_

************
Installation
************

The latest stable release of Tapis CLI is available on PyPi and is the recommended 
way for most people to install it. 

.. code-block:: shell

    $ pip install tapis-cli

Stable but possibly as-yet unreleased updates are available via the `main` branch 
of the Tapis CLI GitHub repository. 

.. code-block:: shell

    $ git clone https://github.com/TACC-Cloud/tapis-cli.git
    $ cd tapis-cli
    $ pip install --user .

***************
Container Image
***************

As an alternative to local installation, the CLI is available as a public
Docker image ``tacc/tapis-cli:latest`` on DockerHub_:

.. code-block:: shell

    docker run --rm -it -v ${PWD}:/work -v ${HOME}/.agave:/root/.agave \
        tacc/tapis-cli:latest bash

********************
Initialize a Session
********************

You must set up a Tapis session on each host where you will use Tapis CLI. This
is a scripted process implemented by ``tapis auth init``. Here's an example:

.. code-block:: shell

    $ tapis auth init

    Use of Tapis requires acceptance of the TACC Acceptable Use Policy,
    which can be found at https://portal.tacc.utexas.edu/tacc-usage-policy

    Do you agree to abide by the AUP? (type 'y' or 'n' then Return) y

    To improve our ability to support Tapis and the Tapis CLI, we would like to
    collect your IP addrress, operating system and Python version. No personally-
    identifiable information will be collected. This data will only be shared in
    aggregate form with funders and Tapis platform stakeholders.

    Do you consent to this reporting? [Y/n]: y

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

***********
Get Started
***********

The CLI features extensive contextual help. Get a listing of
supported commands and global options via  ``--help``.

.. code-block:: shell

    $ tapis --help

Find available commands:

.. code-block:: shell

    $ tapis apps --help
    Command "apps" matches:
    apps create
    apps disable
    apps enable
    apps history
    apps list
    apps pems grant
    ...

Get help for a specific command:

There is a ``--help`` flag for each command.

.. code-block:: shell

    $ tapis help apps list
    $ # or
    $ tapis apps list --help

*************
Issue Tracker
*************

Major functional objectives are bundled into Milestones_ with due dates in the
future. This provides a way to organize the work and have a public road map
for functionality.

All work should proceed through at least one or more reported Issues_.

.. _Milestones: https://github.com/TACC-Cloud/tapis-cli/milestones?direction=asc&sort=due_date&state=open
.. _Issues: https://github.com/TACC-Cloud/tapis-cli/issues


.. |build-status| image:: https://travis-ci.org/TACC-Cloud/tapis-cli.svg?branch=main&style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/TACC-Cloud/tapis-cli

.. |docs| image:: https://readthedocs.org/projects/tapis-cli/badge/?version=latest
    :alt: Documentation
    :scale: 100%
    :target: https://tapis-cli.readthedocs.io/

.. |doi| image:: https://zenodo.org/badge/203083094.svg
    :alt: Publication
    :scale: 100%
    :target: https://zenodo.org/badge/latestdoi/203083094


.. _DockerHub: https://hub.docker.com/r/tacc/tapis-cli/

.. _Tapis: https://agave.readthedocs.io/en/latest/
