###########
Authn/Authz
###########

To initialize a host to use Tapis, run the ``tapis auth init`` command.

.. code-block:: shell

    $ tapis auth init
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

Re-running without changing tenant or username will display the current auth
context, while changing either tenant or username (or specifying
``--interactive`` mode) will re-initialize the host to use the specified
tenant/username combination.

Explicit configuration switching (``tapis auth switch``) is not (yet) supported.

**NOTE** If you have a configured, but expired Agave client in
``~/.agave/current``, the ``init`` command may fail to detect the expiration
and may skip a key step. If you get a message ``Tapis client appears invalid``
re-run with ``tapis auth init --interactive`` and follow the prompts.

*******************************
Manually Specifying Client Name
*******************************

The default behavior for Tapis CLI is to generate and manage one Oauth2 client 
per host you have installed it on. This helps avoid race conditions when you 
might be using the CLI in two places at once. This is done by naming the client 
after your local host. However, this can be a problem if you are using Tapis CLI 
for automation where the hostname may change (such as within Github actions or a 
Jenkins job). In this case, you can manually specify a client name by passing 
``--client-name`` along with ``tapis auth init``. Please note the client name 
must be <= 64 characters and may only contain `A-Za-z0-9` and `. - _`

********
Commands
********

.. autoprogram-cliff:: tapis.cli
   :command: auth *
