################
Template Support
################

Tapis app, job, and system definitions, as well as metadata records, are commonly 
defined as JSON documents stored in files. Sharing these files can be challenging 
(for instance, as part of a collaborative development effort), since they may 
contain user-specific values. Files are also, of course, static assets, so 
any process involving dynamically changing their contents must be automated 
using some form of JSON parsing. Inspired by the solutions our users arrived at 
for these kinds of problems, we have introduced support for templating in Tapis 
CLI. 

This can take the form of simple variable substitution, but since the underlying 
template engine is Python's Jinja2 module, even more sophisticated constructs are 
possible. 

Let us consider an example before diving into details. A group of collabortators each has 
a private copy of a Tapis app for counting chickens, where the app identifier follows the 
naming convention ``chicken-counter-[username]-1.0.0``. They want to standardize on one 
set of parameters for a specific set of chicken counting experiments they are doing. Without 
templating, each would maintain the parameter set in a standalone job file. For user **ellen** 
that file might look like so:

.. code-block:: json

    {
        "appId": "chicken-counter-ellen-1.0.0",
        "archiveSystem": "data-tacc-work-ellen",
        "maxRunTime": "01:00:00",
        "inputs": {
            "chix_img": "agave://data-tacc-cloud/images/too_many_chickens.png"
        },
        "name": "chicken-count",
        "parameters": {
            "beak_threshold": 10.0,
            "wing_threshold": -6.33
        }
    }

If the group leader Francesca decides that ``wing_threshold`` needs to be -8.00, 
everyone needs to edit a copy of their job file. If the group gets their parameter 
files from the group leader, that means they would need to edit out refernces to 
Francesca's username, replacing them with their own. Note also that the job **name** 
is static, which could get annoying. Wouldn't it be nice if we could change it 
for each instance of job that is run? 

Consider a template-based version of this file:

.. code-block:: json

    {
        "appId": "chicken-counter-{{ username }}-1.0.0",
        "archiveSystem": "data-tacc-work-{{ username }}",
        "maxRunTime": "01:00:00",
        "inputs": {
            "chix_img": "agave://data-tacc-cloud/images/too_many_chickens.png"
        },
        "name": "chicken-count-{{ iso8601_basic_short }}",
        "parameters": {
            "beak_threshold": 10.0,
            "wing_threshold": -6.33
        }
    }

Submitting this file to the Tapis jobs service using ``tapis jobs submit`` 
will result in a job request being sent where ``{{ username }}`` is 
replaced with the current Tapis username and ``{{ iso8601_basic_short }}`` 
will be replaced with an IS0-8601 date stamp of format ``YYYMMDDTHHmmss``. 
Nifty, eh? There's much more than can be done with this system!

*********
Variables
*********

There are two classes of variables supported by the template system: 
"core" and "project". Core variables are provided by the CLI with no 
options for user configuration, while project variables are set via 
a file in *.ini* format. 

Core variables
==============

These are, in effect, global variables representing the state and 
environment of the CLI itself. They are intended for use in any app, 
job, system, or metadata definition without additional configuration. 
You can find the name and value of core variables via the command 
``tapis info vals list``. Core variables are snake-cased with no 
dot notation. Examples include ``first_name``, ``fqdn`, 
``git_remote``, and ``username``.

Project Variables
=================

Sometimes, one needs to scope variables to a specific context (i.e. 
only within the build directory for an app). This use case is 
enabled by use of a named *.ini* file. Project variables can be 
identified by use of dot notation in their name. Examples include 
``app.name`` and ``docker.tag``. 

Naming
------

The only supported name for a project variables file is ``project.ini`` 
although ``app.ini`` and ``reactor.ini`` are allowed for backwards 
compatibility with previous versions of the templating system. The 
rationale is that other build systems and applications use the ini 
file format, so we must constrain ourselves to using one name.

Search Path
-----------

If a path is specified using the ``--ini`` option, Tapis CLI looks 
at that location for a project variable file. Note that the file 
**must** be exist and be readable if it is manually specified. If 
no path to an ini file is provided, the CLI looks in the current 
working directory for a file named ``project.ini``. If one is found, 
it must be readable. If no variable file is provided, project 
variables are not made available to the templating system. 

Ini File Schema
---------------

A Tapis CLI ini file contains one or more stanzas: 

    - app : variables pertaining to a Tapis app
    - actor : variables pertaining to a Tapis actor
    - env : general-purpose environment variables
    - git : variables that pertain to a git repository
    - job : variables pertaining to a Tapis job
    - system : variables pertaining to a Tapis system

Within each stanza are named variables. Any variable name included 
in the default ini file (``tapis info vars init``) should be 
considered reserved for use by CLI workflows such as 
``tapis apps deploy`` and ``tapis jobs template``. You are free to 
add additional variables under these sections, with the caveat 
that future updates to the CLI might conflict with them. A better 
solution for defining custom variables is to add them to ``env`` 
as that section is reserved for user- or program-defined data. 

Below is an example ``project.ini`` file. 

.. code-block::

    [app]
    name =
    version =
    bundle =
    deployment_path =
    deployment_system =
    execution_system =

    [actor]
    name =
    description =
    alias =
    stateless = True
    hint =
    privileged = False
    use_uid = True
    workers =

    [docker]
    dockerfile = Dockerfile
    username =
    organization =
    repository =
    tag =
    build_args =
    use_commit_hash = False

    [env]

    [git]
    branch = master
    remote =

    [job]

    [system]
    ssh_private_key = ~/.ssh/id_rsa

**************
Usage Examples
**************

*Coming soon*

*****************
Technical Details
*****************

Tapis CLI uses _Jinja2 to power its template system. Most if not all Jinja 
constructs and syntax should be supported. Please file an _issue if you 
discover that is not the case. 

Tapis CLI uses _Configparser to parse and write ini files. All configparser 
functions, including interpolation (allowing for additional templating 
behavior!), should be available. Please file an _issue if you 
discover that is not the case. 

.. _Configparser: https://docs.python.org/3/library/configparser.html

.. _Jinja2: https://palletsprojects.com/p/jinja/

.. _issue: https://github.com/TACC-Cloud/tapis-cli-ng/issues

