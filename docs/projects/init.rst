##############
Initializing a Project
##############

The CLI supports initialization of a skeleton project, which can be expanded upon 
and further configured by the developer. These projects are based on template 
source code repositories written using the CookieCutter specification. The 
steps taken by the CLI to create a skeleton project are the same for each class of 
project (app, actor, etc.):

    1. Clone the relevant template repository into a bare directory, named by the user.
    2. Write out contents of the repository, filling in contents of template variables known to the CLI
    3. Initialize the directory as a new Git repository.
    4. Add the initial set of files and commit to the repository
    5. Create an instance of the repository on the user's Git server
    6. Set that repository as the ``remote`` for the current local repository

*********************
The source repository
*********************

Each kind of project has its own default source repo which contains one or more templates. One of 
the templates is designated as the **default**.  The idea is that an ``init`` command is run without 
specifying a repo and/or template, a perfectly servicable skeleton project will be 
instantiated. Specifying other template names will create projects with different configurations, as 
defined by the source repository.  More details on the CookieCutter standard, which is used to define 
repository templates can be found elsewhere in the documentation.  

The most essential fact for you to know is that you can find out the names of every kind of template 
for a given source repository from the **Templates** table in the repository's README document. 

***************
Initialize an app
***************

*Coming soon*

*****************
Initialize an actor
*****************

*Coming soon*

