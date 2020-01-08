########
Projects
########

There are many good designs and patterns for building 
cloud-based applications. In the Linux container world, we have 
a choice of hand-crafting a set of linked services or using 
some of the declarative tooling like Docker stacks or Kubernetes 
pods. These can be deployed to any number of on-prem or 
public platforms. At a higher level of abstraction, systems such 
as Pantheon and Heroku promote one-command definition and deployment 
of web applications and services, which is achieved, in part, 
through use of simple configuration files coupled with a connection 
to the deployment host. These systems advance the promise of 
maintainability and reusability offered by containers, package 
registries, source code managers, config management tools, and 
hosted deployment environments. 

We have adopted some of the best practices from popular systems and 
platforms to make it easy to build, deploy, and maintain Tapis apps 
and actors. One of these practices to offer a robust 
and usable CLI. Another is to allow automation of common tasks to 
enable reusability and decrease user error. To 
this end, the Tapis CLI features a **deploy** subcommand for the 
**apps** and **actors** APIs. The concept is that every 
step required in deploying a Tapis resource should be achievable by 
cd-ing into a project directory and running ``tapis apps deploy`` or 
``tapis actors deploy``

.. toctree::
   :maxdepth: 1

   structure
   app_ini
   init
   deploy.rst
   git.rst
