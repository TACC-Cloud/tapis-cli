######################
Initializing a Project
######################

The CLI supports initialization of a skeleton app and actor projects. These are 
based on templates written using the CookieCutter specification and housed in 
a public Github repository. 

*************************
Initialize an app project
*************************

The ``tapis apps init`` command will create a new app for you following the designated 
template. You may specify some basic details of the initial configuration, such as the 
app name, human-readable label, verbose description, and semantic version, when 
creating a new app project. Some details are inherited from the CLI settings, such 
as your preferred Docker namespace and registry. 

Here is an example of creating a new app from the **default** template

.. code-block:: shell

    $ tapis apps init --app-name Appy --app-label APPINESS --app-description \
      "I am appy to see you" --template default

    +-------+---------------------------------------------------------------+
    | stage | message                                                       |
    +-------+---------------------------------------------------------------+
    | setup | Project path: ./appy                                          |
    | setup | CookieCutter variable name=Appy                               |
    | setup | CookieCutter variable description=I am appy to see you        |
    | setup | CookieCutter variable project_slug=appy                       |
    | setup | CookieCutter variable docker_namespace=sd2e                   |
    | setup | CookieCutter variable docker_registry=https://index.docker.io |
    | clone | Project path: ./appy                                          |
    +-------+---------------------------------------------------------------+

If you want to preflight the values that the ``init`` system is going to use 
to create a new project, you can pass the ``--dry-run`` command flag. The CLI will 
run all the setup steps, printing the results to screen, but will not actually 
create the project.  

Once you have your new app project, you can configure and customize the app by 
editing its ``project.ini``, ``app.json``, or ``run.sh`` files. You can, if the
app is container-based, modify the Dockerfile that specifies the app's digital 
assets, or you can package software and dependencies directly in the app's 
``assets`` directory. 

You can manually upload the app and register it in the Tapis system using 
individual CLI commands such as ``tapis files upload`` and ``tapis apps create`` or 
(probably preferably), you can use the ``tapis apps deploy`` command which bundles all 
necessary Tapis operations into a simple workflow. 

---------------------
Finding app templates
----------------------

You can list the catalog of available templates by passing the ``--list-templates`` 
command flag:

.. code-block:: shell

    $ tapis app init --list-templates
    +-----------+--------------+------------------------------------------+----------+
    | id        | name         | description                              | level    |
    +-----------+--------------+------------------------------------------+----------+
    | default   | Default      | Basic code and configuration skeleton    | beginner |
    | shellrun  | Shell Runner | Run an arbitrary shell command via Tapis | beginner |
    | wordcount | Word Count   | Simple word counting implementation      | beginner |
    +-----------+--------------+------------------------------------------+----------+

Pass one of the listed **id** values to the ``--template`` flag when to initialize 
a new Tapis app based on that template. Further instructions will be included in a 
README file in the new project directory.

If you have access to an alternate repository of CookieCutter templates (perhaps provided 
by your Tapis tenant operator) you can specify its URL via the ``--repo`` flag. You can also 
specifiy a specific commit or branch on the repository via the ``--checkout`` flag. 

***************************
Initialize an actor project
***************************

*Coming soon*


*********************
Template repositories
*********************

The Tapis CLI uses a public repository containing subdirectories, where each subdirectory is a 
project template implemented using the **CookieCutter** specification. There is always a template 
named **default** which the CLI is configured to use if no other template is specified. 

When a project is created from a CookieCutter template, the CLI uses a collection of 
key-value variables to fill out file names and contents in the new directory. Some of these, 
as mentioned above, are specified at the command line and some are based on values available 
via ``tapis config``. 

Details on how to report issues, request improvements, or contribute new templates can be found 
in the README of each templates repository, and such contributions are welcomed. 
