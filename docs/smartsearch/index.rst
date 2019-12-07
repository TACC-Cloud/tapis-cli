###############
Search Commands
###############

Several Tapis command families support sophisiticated search capabilities, but
due to the fact that Tapis has been developed over several years,
implementation details of syntax and capability vary widely. Tapis CLI remedies
this with named **search** commands which accept optionized forms of select
top-level keys for each supported service. Limited support for types and
enumerations is presented as well, as well as support for search modifiers.
Finally, semantic or "humanized" dates are ranges are supported as query terms
in fields which are Python ``datetime`` types.

**********
An Example
**********

To stimulate your interest, here's a simple example of searching for an app by a
fragment of its name. The generalized form of a Tapis CLI search command is
``tapis <service> search --field-name <modifier> <value>``.

.. code-block:: shell

    $ tapis apps search --name like image
    +-------------------------------+----------+------------------+-------------------------------+----------+------------------------+
    | id                            | revision | label            | shortDescription              | isPublic | executionSystem        |
    +-------------------------------+----------+------------------+-------------------------------+----------+------------------------+
    | tapis.app.imageclassify-1.0u3 |        3 | Image Classifier | Classify an image using a     | True     | tapis.execution.system |
    |                               |          |                  | small ImageNet model          |          |                        |
    | tapis.app.imageclassify-1.0u2 |        2 | Image Classifier | Classify an image using a     | True     | tapis.execution.system |
    |                               |          |                  | small ImageNet model          |          |                        |
    | tapis.app.imageclassify-1.0u1 |        1 | Image Classifier | Classify an image using a     | True     | tapis.execution.system |
    |                               |          |                  | small ImageNet model          |          |                        |
    +-------------------------------+----------+------------------+-------------------------------+----------+------------------------+

*******************
Search help strings
*******************

The code that enables search also generates descriptive, if a bit
repetitive, help text for each search command. The help text for
**systems search** is shown below, followed by a few notes to help you
make sense of what you are seeing seen. The help for any **search** command
will yield similar detailed instructions.

.. code-block:: shell

   $ tapis systems search -h
   usage: tapis systems search [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                                [--quote {all,minimal,none,nonnumeric}]
                                [--noindent] [--max-width <integer>] [--fit-width]
                                [--print-empty] [--sort-column SORT_COLUMN]
                                [--no-verify] [-z <token>] [-l <int>] [-o <int>]
                                [--available eq*|neq true|false]
                                [--default eq*|neq true|false]
                                [--description eq*|neq|start|end|like <string>]
                                [--execution-type eq*|neq CLI|Condor|HPC]
                                [--global-default eq*|neq true|false]
                                [--id eq*|neq|start|end|like <string>]
                                [--max-system-jobs eq*|neq|gt|gte|lt|lte <int>]
                                [--max-system-jobs-per-user eq*|neq|gt|gte|lt|lte <int>]
                                [--name eq*|neq|start|end|like <string>]
                                [--owner eq*|neq|start|end|like <string>]
                                [--public eq*|neq true|false]
                                [--revision eq*|neq|gt|gte|lt|lte <int>]
                                [--scheduler eq*|neq|start|end|like CONDOR|CUSTOM_SLURM|FORK|LSF|PBS|SGE|SLURM]
                                [--status eq*|neq DOWN|MAINTENANCE|UNKNOWN|UP]
                                [--type eq*|neq EXECUTION|STORAGE]

Picking a few representative fields, we see:

- **description** is a string. The recommended search modifier is **eq** and the expected value is any string.
- **executionType** is a string, but has constrained values of ``CLI``, ``Condor``, or ``HPC``
- **available** is a Boolean. You can construct a positive or negative filter with equals, not-equals, true, and false
- **maxSystemJobs** is an integer. You can use direct (eq, ne) as well as quantitative comparisons (lt, gte, etc.)

Modifiers
---------

This is the canonical list of modifiers and the search pattern they attempt
to implement for their respective web service and parameter.

+----------+-------------------------------------+-------------------------+
| Modifier | Explanation                         | Types                   |
+----------+-------------------------------------+-------------------------+
| eq       | Equals                              | String, Number, Boolean |
+----------+-------------------------------------+-------------------------+
| neq      | Does not equal                      | String, Number, Boolean |
+----------+-------------------------------------+-------------------------+
| like     | Contains                            | String                  |
+----------+-------------------------------------+-------------------------+
| start    | Starts With                         | String                  |
+----------+-------------------------------------+-------------------------+
| end      | Ends With                           | String                  |
+----------+-------------------------------------+-------------------------+
| gt, gte  | Greater than (or equal)             | Number                  |
+----------+-------------------------------------+-------------------------+
| le, lte  | Less than (or equal)                | Number                  |
+----------+-------------------------------------+-------------------------+
| on       | After 00:00 but before 11:59:59 UTC | Date                    |
+----------+-------------------------------------+-------------------------+
| before   | Before 0:00 UTC                     | Date                    |
+----------+-------------------------------------+-------------------------+
| after    | After 11:59:59 UTC                  | Date                    |
+----------+-------------------------------------+-------------------------+

Human Dates
-----------

Here are some examples of humanized dates for searching date fields.

+--------------------------+-------------------------------------------+
| Example                  | Span                                      |
+--------------------------+-------------------------------------------+
| before today             | Prior to today                            |
+--------------------------+-------------------------------------------+
| after "this week"        | Within the current week, marked by Sunday |
+--------------------------+-------------------------------------------+
| after "October 15, 2018" | After midnight UTC Oct 15, 2018           |
+--------------------------+-------------------------------------------+
| gte "2 hours"            | More than 2 hours ago                     |
+--------------------------+-------------------------------------------+
| after "6/1/2019"         | After midnight June 1, 2019               |
+--------------------------+-------------------------------------------+
| after 2018               | Any time in 2019 or after                 |
+--------------------------+-------------------------------------------+

*************************
Search support by command
*************************

Search is available for several commands, and is on the roadmap for 
a few more in the coming months.

+----------------+--------------+
| Command Family | Smart Search |
+----------------+--------------+
| auth           | No           |
+----------------+--------------+
| actors         | Planned      |
+----------------+--------------+
| apps           | Yes          |
+----------------+--------------+
| files          | Planned      |
+----------------+--------------+
| git            | Planned      |
+----------------+--------------+
| hooks          | No           |
+----------------+--------------+
| jobs           | Yes          |
+----------------+--------------+
| metadata       | Yes          |
+----------------+--------------+
| notifications  | Planned      |
+----------------+--------------+
| profiles       | Yes          |
+----------------+--------------+
| settings       | No           |
+----------------+--------------+
| status         | Planned      |
+----------------+--------------+
| systems        | Yes          |
+----------------+--------------+
| versions       | No           |
+----------------+--------------+

