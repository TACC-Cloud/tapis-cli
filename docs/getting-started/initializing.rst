Initialize a Session
====================

You must set up a Tapis session on each host where you will use Tapis CLI. This
is a scripted process implemented by ``tapis auth init``. The first time you
run this command on a new host, you will be shown an introductory screen
where we ask two questions of you. Future invocations of the ``init`` command
will not display these messages unless their contents change. You will then
be prompted for tenant, username, and password required to set up a session.

.. code-block:: shell

    $ tapis auth init

    Use of Tapis requires acceptance of the TACC Acceptable Use Policy 
    which can be found at https://portal.tacc.utexas.edu/tacc-usage-policy

    Do you agree to abide by the AUP? (type 'y' or 'n' then Return) y

    Use of Tapis requires acceptance of the Tapis Project Code of Conduct
    which can be found at https://tapis-project.org/code-conduct

    Do you agree to abide by this CoC? (type 'y' or 'n' then Return) y

    To improve our ability to support Tapis and the Tapis CLI, we would like to
    collect your IP address, operating system and Python version. No personally-
    identifiable information will be collected. This data will only be shared in
    aggregate form with funders and Tapis platform stakeholders.

    Do you consent to this reporting? [Y/n]: Y

    Tapis API access
    ################
    Available Tenants
    *****************
    3dem	agave.prod	araport.org	bridge	designsafe
    iplantc.org	irec	portals	sd2e	sgci
    tacc.prod	vdjserver.org

    Enter a tenant name: tacc.prod
    Username: tacotron
    Password for tacotron:
    Container registry access
    #########################
    Registry Url [https://index.docker.io]:
    Registry Username []: tacotron
    Registry Password []:
    Registry Namespace []: TACO
    Git server access
    #################
    Git Url [https://github.com]:
    Git Username []: taconaut
    Git Token []: 
    Git Namespace []: TACOS

    +--------------------+---------------------------------+
    | Field              | Value                           |
    +--------------------+---------------------------------+
    | tenant_id          | tacc.prod                       |
    | username           | tacotron                        |
    | client_name        | _cli-tacc.prod-tacotron-macbook |
    | api_key            | uAShaDfy0vF7hgFcAqx7oeAtO6oa    |
    | access_token       | a31c66cfaa45451c95df6fd473ffd4b |
    | expires_at         | Thu Sep 19 14:08:37 2019        |
    | registry_url       | https://index.docker.io         |
    | registry_username  | tacotron                        |
    | registry_password  | T0rchy$                         |
    | registry_namespace | tacotron                        |
    | git_url            | https://github.com              |
    | git_username       | tacomatic                       |
    | git_token          | hqd8kw59h2h5z4zw78e64qz9        |
    | git_namespace      | TACOS                           |
    +--------------------+---------------------------------+


Getting Help
------------

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
