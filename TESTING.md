# Overview

Tapis CLI implements a (hopefully) consistent grammar and syntax: `tapis
<service> <entity> <action>`. In cases where there's nested
functionality (such as with permissions), the command structure is
`tapis <service> <entity> <sub-entity> <action>`.

  - Search and discovery actions:
      - list - generic list of known entities
      - search - parameterized search of known entities
      - show - display full record for one known entity

  - File management:
    - download - fetch Tapis remote asset(s) to local storage
    - upload - send asset(s) to Tapis from local storage

  - Management actions:
      - create - create a new entity
      - update - update an existing entity by identifier
      - delete - delete an entity by identifier
      - disable - temporarily remove a resource from use
      - enable - restore a resource to use
      - publish - make a resource publicly usable
      - unpublish - remove a resource from public use
      - hide - hide a resource (jobs only) from view
      - unhide - restore visibility to a resource (jobs only)

  - Permissions and roles:
      - list - list entitlements for entity by identifier
      - show - display a specific entitlement by identifier and username
      - grant - assign a role or permission for a username to an entity
      - revoke - remove role or permission for a username from an entity
      - drop - remove all granted roles/permissions from an entity

# What To Test

This tool is designed to completely (and quickly - by Q42019) replace
our legacy Bash tooling. So, our general request is to get in there an
exercise it like you would the legacy CLI. But, specific new features
that testers can help review on are laid out below by service.

## Known Issues

The following are **known issues** and will be addressed in future work periods:

> 1.  ~~Python 2.7.x is not supported (but will be)~~ (18-10-2019)
> 2.  ~~No **files** commands are implemented~~
> 3.  No **actors** or **tacclab** commands are implemented
> 4.  The **watch** function from the old jobs-submit is gone and will
>     never return
> 5.  ~~Impersonation token issuance is not yet implemented~~
> 6.  The beloved `auth switch` is not yet implemented
> 7.  Metadata schema and ~~record management~~ commands are not yet
>     implemented
> 8.  No **notifications** commands are implemented
> 9.  The module is not yet available on PyPi
> 10. Documentation builds are broken
> 11. Creation of the Bash autocomplete config is broken
> 12. ~~Search on dates is broken~~
> 12. ~~Search on booleans can be broken (try `--boolean eq true`)~~
> 13. ~~Access tokens passed via `-z` or `--token` are not honored~~
> 14. Some `pems drop` commands do not actually drop all granted permissions
> 15. Commands built with AgavePy don't report complete error messages

## Installation

04-10-2019 | The latest Docker image build of `master` is now always
available as `tacc/tapis-cli-ng:latest` within 15-30 minutes after a commit
is pushed to `master`. This is now accomplished via a Travis CLI workflow
rather than by manual intervention by the developers.

20-09-2019 | The CLI is installable from git checkout
  - It must be installable in **editable** mode (`pip install -e
    .`)
  - It must be installable in a virtual environment
  - It must be installable using setuptools (`python setup.py
    install`)
  - It must be installable under Python 3.5, 3.6, and 3.7
  - It must be installable under Python 2.7.15+

Please test the CLI under your favorite Python enviroment
management practices so we can make sure it's relatively robust for
the end user communities that will use it.

## General CLI Capabilities

  - The name of every command must be intuitive and aligned with its
    function and (where possible) directly congruent with the underlying
    API functionality. I realize this is a matter of opinion, but its
    still a hard requirement.
  - Every command must have descriptive and accurate help text. This
    includes the command description and all options.
  - All commands must display a JSON response when run using the `-v`
    flag
  - Commands that list multiple records must implement `--limit` and
    `--offset` and those arguments should work as indicated
  - Commands that display a specific record follow the form `tapis <api>
    show <identifier>`. The name and description for each API's
    identifier must be correct. For instance, the name and description
    for Apps are `<app_id>` and `App identifer`, respectively
  - Commands that access Tapis APIs must support specification of access
    token via `-z` or `--token`. A valid token should always work, even
    if its an impersonation token. Invalid tokens should fail.
  - Commands that access Tapis APIs must allow base URL to be overridden
    via the `-H` option
  - The CLI must fail gracefully when networking is not available

## Configuration

01-11-2019 | There is now support for setting, unsetting, and getting
specific `.env` based settings for the CLI. Here's an example:

```$ tapis settings get TAPIS_CLI_PAGE_SIZE
+---------------------+-------+
| Field               | Value |
+---------------------+-------+
| TAPIS_CLI_PAGE_SIZE | 33    |
+---------------------+-------+

$ tapis settings set TAPIS_CLI_PAGE_SIZE 50
+---------------------+-------+
| Field               | Value |
+---------------------+-------+
| TAPIS_CLI_PAGE_SIZE | 50    |
+---------------------+-------+

11-10-2019 | The behavior for finding a `.env` has been clarified. The CLI
searches the current working directory, followed by `$HOME` for an environment
file. The expected path for the CLI's environment file can be discovered via
`tapis settings list` as `_ENV_PATH`.

All environment settings specific to the Tapis CLI are now explicitly
prefixed by `TAPIS_CLI_` in the configuration files. Settings variables
imported from other modules (such as AgavePy) have their own namespace,
such as `TAPIS_PY_` or simply `TAPIS_`. See `.env.sample` for clarification.

It is now possible to specify a tenants server and default
`tenant_id` for a non-TACC installation of the CLI. This accomplished by
setting the variables `TAPIS_TENANTS_URL` and `TAPIS_DEFAULT_TENANT_ID`,
respectively. Note that setting the default identifier will only change
the behavior of `tapis auth init` by setting the designated value as the
default value for `--tenant-id` in the interactive prompt.

Several unused configuration settings were deactivated, including some
pertaining to JupyterHub, Gitlab, and Tapis tenancy.

Settings are now presented in alphabetically-sorted order.

04-10-2019 | The CLI leverages `python-dotenv` for configuration via file.
This is currently used to control a couple of features, outlined below. An
example config file can be found in `.env.sample` in the Github repo. The
config file must be named `.env` but can be placed in the current working
directory or the user's `$HOME` directory.

Two configuration options to note include `TAPIS_CLI_FIT_WIDTH` which sets
whether the CLI automatically formats its tables to the current terminal
width. The other is `TAPIS_PY_SHOW_CURL` which toggles live display of all
API requests made by the CLI formatted as `cURL` commands.

20-09-2019 | The CLI uses .env files and environment variables to configure
some persistent settings. This will be described in more detail in
future testing sessions.

## Display Options

01-11-2019 | There is a new configuration option `TAPIS_PY_VERBOSE_ERRORS`
which controls whether the contents of a Tapis API server message is
returned as part of the general `HTTPError` that is raised when an
error is encountered. The default is `True` but can be disabled in case the
new function introduces a regression somewhere. Here's an example of trying to
show a non-existent App. Before this new capability was released, the 404
would have been reported simply as a client error. Now, a more informative
response is provided.

```shell
$ tapis apps show sd2etest-xea-test-0.0.2
[Errno 404] Not Found for https://api.sd2e.org/apps/v2/sd2etest-xea-test-0.0.2: 'No software found matching sd2etest-xea-test-0.0.2'
```

Here's another example, where an attempt is made to submit an invalid
App definition.

```shell
$ tapis apps create -F tests/data/commands/apps/simple-app-invalid.json
[Errno 400] Bad Request for https://api.sd2e.org/apps/v2/: "Invalid 'app.name' value. Please enter a valid name for this app."
```

25-10-2019: A point of clarification: You should probably just set
`TAPIS_PY_SHOW_CURL` and allow it to govern the CLI's behavior.

11-10-2019 | AgavePy has been updated to also print cURL-equivalent commands to
STDERR. This behavior can be toggled by setting `TAPIS_PY_SHOW_CURL=1` in the
environment or relevant `.env` file. `TAPIS_CLI_SHOW_CURL` now defaults to the
value of `TAPIS_PY_SHOW_CURL` allowing both CLI and AgavePy clients to be
toggled with a single setting.

04-10-2019 | New in this version is support for printing the curl equivalent
for some commands to STDERR. This can be toggled on by setting
`TAPIS_CLI_SHOW_CURL=1` in the environment or in the relevant `.env` file.
Note that only commands that use the `TaccApiDirectClient` class to
interact with Tapis currently have this capability.

## Auth

04-10-2019 | It is now possible for users with the proper administrative role
to generate impersonation tokens. The impersonation token is not written to
the local credential cache. Here is an example:

```shell
$ tapis auth tokens create --token-username vaughn
Password:
+--------------+---------------------------------+
| Field        | Value                           |
+--------------+---------------------------------+
| access_token | a207c7f0beec4757244e3b4460d917f |
| username     | vaughn                          |
+--------------+---------------------------------+
```

Access tokens (both personal and impersonation) are now properly honored when
passed to commands via the `-z` or `--token` option.

27-09-2019 | No changes

20-09-2019 | This release marks debut of a simplified authentication workflow
targeted at end users. In the new approach, one host-specific client is
generated and maintained for each combination of tenant and username. To
initialize a host to use Tapis, simply run the `tapis auth init`
command. Re-running it without changing tenant or username will simply
display the current auth context. Changing either of those values, or
specifying `--interactive` mode will re-initialize the host to use the
new tenant/username combination.

The `tapis auth show` command will display the current auth state, without
taking any action to update the Oauth token.

Token management should be much less manual than it has become in recent
months with the Bash CLI, in that you should almost never have to
manually create or refresh or a token. Should you need to do so, the
commands for doing so are `tapis auth tokens create` and `tapis auth
tokens refresh`

Switching between profiles ( `tapis auth switch`) is not currently
supported.

## Apps

01-11-2019 | It is now possible for an admin user to specify the name and
version when publishing an App.

It is now possible to clone an existing App using `tapis apps clone...`

04-10-2019 | Boolean search options are functional. Search arguments where
there are a restricted set of choices are now indicated in the help. Note that
Search on date fields is not supported. The preferred modifier for each
argument is now highlighted. See example below:

```shell
$ tapis apps search -h
usage: tapis apps search [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                         [--quote {all,minimal,none,nonnumeric}] [--noindent]
                         [--max-width <integer>] [--fit-width] [--print-empty]
                         [--sort-column SORT_COLUMN] [--no-verify]
                         [-z <token>] [-l <int>] [-o <int>]
                         [--id eq*|neq|start|end|like <string>]
                         [--name eq*|neq|start|end|like <string>]
                         [--version eq*|neq|start|end|like <string>]
                         [--revision eq*|neq|gt|gte|lt|lte <int>]
                         [--label eq*|neq|start|end|like <string>]
                         [--short-description eq*|neq|start|end|like <string>]
                         [--long-description eq*|neq|start|end|like <string>]
                         [--owner eq*|neq|start|end|like <string>]
                         [--public eq*|neq true|false]
                         [--execution-type eq*|neq|start|end|like CLI|HPC]
                         [--execution-system eq*|neq|start|end|like <string>]
                         [--deployment-system eq*|neq|start|end|like <string>]
                         [--available eq*|neq true|false]
                         [--parallelism eq*|neq|start|end|like PARALLEL|SERIAL]
                         [--default-processors-per-node eq*|neq|gt|gte|lt|lte <int>]
                         [--default-memory-per-node eq*|neq|gt|gte|lt|lte <int>]
                         [--default-node-count eq*|neq|gt|gte|lt|lte <int>]
                         [--default-max-run-time eq*|neq|start|end|like <string>]
                         [--default-queue eq*|neq|start|end|like <string>]
```

27-09-2019 | No changes

20-09-2019 | Feel free to exercise the entire *apps* lifecycle save for cloning. Creation,
updating, publishing, search & discovery, and sharing are all implemented.

## Jobs

25-10-2019 | Job permissions management commands are now supported. Job  UUIDs
are soft-validated for length and suffix characters.

Jobs can now be hidden and unhidden via `tapis jobs hide/unhide`. A job cannot
be listed or viewed when hidden. This is provided as an alternative to
deleting the job, which is antithetical to provenance and usage tracking.

04-10-2019 | Boolean search options are functional. Search arguments where
there are a restricted set of choices are now indicated in the help. The
preferred modifier for each argument is now highlighted. Furthermore, date
search, including support for semantic dates and humanized data strings is
implemented. Some usage examples include:

```shell
# Show recent completed jobs launched yesterday
$ tapis jobs search --status eq FINISHED -l 10 --created on yesterday
# Show failed jobs created before yesterday (09/30/2019)
$ tapis jobs search --status eq FAILED -l 10 --created before "Sep 30, 2019"
# Jobs derived from the word-count-0.1 app template this year
$ tapis jobs search --app-id eq word-count-0.1 --limit 5 --created after 1/1/2019
```

Wildcard support for selecting which output files to download is now
available via the `--include` and `--exclude` options. Here is an example:

```shell
tapis jobs outputs download 8236380857915871721-242ac11d-0001-007 \
      --sync --debug  --exclude "*.err" --exclude "*.out" --exclude "*.pid"
```

27-09-2019 | Implementations of the legacy `jobs-output-list` and `jobs-output-get` commands
are now available. Note the added flexibility in the `tapis jobs outputs download`
command:
* Download to the current directory via `--cwd` option
* Force overwrite of local files with `--force`
* Overwrite local files only of different with `--sync`
* Report progress to STDERR with `--progress`
* Specify remote files to skip with the `--exclude` option

The following downloads outputs from a designated job to the current working
directory, ignoring any files that seem to have already been downloaded. The
command reports a table, as shown below. One of the source files (`wc-sample.txt`)
has already been downloaded so will be intentionally skipped.

```shell
$ tapis jobs outputs download 9e74b852-0e1f-4363-8c09-5ab9f5299797-007 --cwd --sync
+-------------+-------+
| Field       | Value |
+-------------+-------+
| downloaded  | 4     |
| skipped     | 1     |
| warnings    | 0     |
| elapsed_sec | 5     |
+-------------+-------+
```

The `-v` verbose view enumerates each the outcome of each attempted download.

```json
{
  "downloaded": [
    "/20190221t174839.err",
    "/20190221t174839.out",
    "/20190221t174839.pid",
    "/wc_out/output.txt"
  ],
  "skipped": [
    "/wc-sample.txt"
  ],
  "warnings": [],
  "elapsed_sec": 1
}
```

20-09-2019 | Key Aloe *jobs* functions are implemented save for permission management,
hide, and unhide. One interesting new feature of `tapis jobs show` is the `-T`
option, which will translate the verbose Aloe jobs output into a JSON
request document that can be used to submit a similar job.

## Files

25-10-2019 | It is now possible to define the destination path in
`tapis files download`.

11-10-2019 | Permissions management commands for files are now implemented
The syntax is `files pems <action> <agave_url> <username> [<permission>]`

The following additional files management commands are implemented: `files mkdir`

04-10-2019 | File deletion is now supported. File history is now supported.

27-09-2017 | File listing, inspection, and downloads (including recursive) are
now implemented. File uploads are also working. Here is an example sample
files list operation:

```shell
$ tapis files list agave://data-sd2e-community/sample/tacc-cloud
+----------------------------------+---------------------------+--------+
| name                             | lastModified              | length |
+----------------------------------+---------------------------+--------+
| 0R56K8E3WTJJVEV8ZBR31LYTJFDWRKYC | 2019-08-07 10:18:54-05:00 |   4096 |
| README.rst                       | 2019-06-27 15:43:05-05:00 |   1516 |
| S49HDZ458N75SD46AXPA8TJTCO02UBFH | 2019-08-07 10:18:53-05:00 |   4096 |
| agavehelpers                     | 2019-09-23 13:00:32-05:00 |   4096 |
| compat-upload                    | 2019-07-16 15:11:43-05:00 |   4096 |
| dawnofman.jpg                    | 2019-08-07 07:18:49-05:00 | 119974 |
| issue15                          | 2019-08-07 10:19:02-05:00 |   4096 |
| sampleset                        | 2019-06-05 14:55:30-05:00 |   4096 |
| wc-sample.txt                    | 2019-08-07 07:19:02-05:00 |   2846 |
| yakshave.png                     | 2019-07-16 15:11:41-05:00 | 426008 |
+----------------------------------+---------------------------+--------+
```

Here is an example of the download function:

```shell
$ tapis files download --progress agave://data-sd2e-community/sample/tacc-cloud
Walking remote resource...
Found 8 file(s) in 11s
Downloading jazzcat.jpg...
Downloading hello.txt...
Downloading yakshave.png...
Downloading dawnofman.jpg...
Downloading README.rst...
Downloading samples_nc.json...
Downloading wc-sample.txt...
Downloading yakshave.png...
Downloaded 8 files in 10s
+-------------+-------+
| Field       | Value |
+-------------+-------+
| downloaded  | 8     |
| skipped     | 0     |
| warnings    | 0     |
| elapsed_sec | 21    |
+-------------+-------+
```

Uploading to Tapis files is now much improved over the Bash CLI:
* files and folders can be explicity included or excluded via named options
  * wildcard characters are supported in the include and exclude options
* total data movement and time elapsed are reported, just like downloads
* recursive uploads are handled automatically now

Here is an example upload command where an entire directory is uploaded,
excluding files that match the string "ink".

```shell
$ tapis files upload agave://data-sd2e-community/sample/tacc-cloud \
        tests/data/commands  -v --debug --exclude "*ink*" --progress
Finding file(s) to upload...
Found 4 file(s) in 0s
Creating remote directory "commands"...
Creating remote directory "commands/files"...
Creating remote directory "commands/jobs"...
Creating remote directory "commands/apps"...
Uploading tests/data/commands/files/ink.jpg...
Uploading tests/data/commands/jobs/word-count-job.json...
Uploading tests/data/commands/apps/simple-app.json...
Uploading tests/data/commands/apps/word-count-app.json...
Uploaded 3 files in 2s
{
  "uploaded": [
    "tests/data/commands/jobs/word-count-job.json",
    "tests/data/commands/apps/simple-app.json",
    "tests/data/commands/apps/word-count-app.json"
  ],
  "skipped": [
    "tests/data/commands/files/ink.jpg"
  ],
  "warnings": [
    "tests/data/commands/files/ink.jpg matched exclude filter"
  ],
  "data": 5483,
  "elapsed_sec": 2
}
```

## Systems

04-10-2019 | Boolean search options are functional. Search arguments where
there are a restricted set of choices are now indicated in the help. Searches
on date fields is not supported. The preferred modifier for each argument is
now highlighted. See example below:

```shell
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
```

27-09-2019 | No changes

20-09-2019 | Core Tapis *systems* functions are implemented. Queue management is still missing as
is the ability to atomically update a system's login inforamation.

## Metadata

25-10-2019 | Metadata permissions management commands are now supported. Metadata UUIDs
are soft-validated for length and suffix characters.

11-10-2019 | Creation, update, and delete for metadata records is now supported. A (hopefully)
improved workflow is now supported for create and update.

The *name* and *value* keys in metadata documents have been embraced fully,
allowing `name` to be used as a search term for specific documents. Rather
than requiring a JSON document to create a metadata record, one can now
be synthesized by passing the contents as  `--value`.

In addition to using command line options, the contents of a JSON file can
be loaded. There are two formats these JSON files can take. In the first, the
`name` and `value` are specified as top-level keys. In the second, the
contents of the JSON file are interpreted to be the value for the document and
the document name must either be provided or automatically generated.

At create time, the *name* of a document can be specified in one of three ways:
1. Explicitly, using the `--name` option
2. Explicitly by setting a `name` key in the source JSON file
3. Automatically from Tapis username, a hash of the document's `value`, and a timestamp

When updating a document by UUID, the default behavior is to maintain the
existing *name*, even if the document's `value` key changes (and the timestamp
has obviously changed). This can be over-ridden by specifying the `--rename`
option or by including the new value in a `name` key in the source JSON document.

### Examples

Here are some sample command/response sequences for `tapis metadata create`:

```shell
# Note that --name is not provided and is thus autogenerated
$ tapis metadata create --value "This is a test"
+-------------+----------------------------------------+
| Field       | Value                                  |
+-------------+----------------------------------------+
| uuid        | 4133438794726436375-242ac11a-0001-012  |
| owner       | vaughn                                 |
| name        | vaughn.f16204ef7ed05949.191010T173121Z |
| value       | This is a test                         |
| created     | just now                               |
| lastUpdated | just now                               |
+-------------+----------------------------------------+

# Explicitly name the new document...
$ tapis metadata create --value "This is another test" --name "11102019.demo"
+-------------+---------------------------------------+
| Field       | Value                                 |
+-------------+---------------------------------------+
| uuid        | 1111886352317476375-242ac11a-0001-012 |
| owner       | vaughn                                |
| name        | 11102019.demo                         |
| value       | This is another test                  |
| created     | just now                              |
| lastUpdated | just now                              |
+-------------+---------------------------------------+

# Automatically generate name for an anonymous JSON object in a file
$ tapis metadata create -F anonymous-object.json
+-------------+----------------------------------------+
| Field       | Value                                  |
+-------------+----------------------------------------+
| uuid        | 7095279578129362455-242ac11a-0001-012  |
| owner       | vaughn                                 |
| name        | vaughn.d021c9f2e90369e3.191010T173722Z |
| value       | {'info': 'This is an anoymous object'} |
| created     | just now                               |
| lastUpdated | just now                               |
+-------------+----------------------------------------+
```

Here are some sample command/response sequences for `tapis metadata update`:

```shell
# Update a document's value. Note that the name doesn't change.
$ tapis metadata update -V "This value was changed" 1111886352317476375-242ac11a-0001-012
+-------------+---------------------------------------+
| Field       | Value                                 |
+-------------+---------------------------------------+
| uuid        | 1111886352317476375-242ac11a-0001-012 |
| owner       | vaughn                                |
| name        | 11102019.demo                         |
| value       | This value was changed                |
| created     | 8 minutes ago                         |
| lastUpdated | just now                              |
+-------------+---------------------------------------+

# Document has been updated and renamed
$ tapis metadata update -V "This value was changed again" \
  --rename "11102019.demo.2" 1111886352317476375-242ac11a-0001-012
+-------------+---------------------------------------+
| Field       | Value                                 |
+-------------+---------------------------------------+
| uuid        | 1111886352317476375-242ac11a-0001-012 |
| owner       | vaughn                                |
| name        | 11102019.demo.2                       |
| value       | This value was changed again          |
| created     | 9 minutes ago                         |
| lastUpdated | just now                              |
+-------------+---------------------------------------+

# Update from contents of a file, retaining name
$ tapis metadata update -F anonymous-object-update.json 7095279578129362455-242ac11a-0001-012
+-------------+------------------------------------------------+
| Field       | Value                                          |
+-------------+------------------------------------------------+
| uuid        | 7095279578129362455-242ac11a-0001-012          |
| owner       | vaughn                                         |
| name        | vaughn.d021c9f2e90369e3.191010T173722Z         |
| value       | {'info': 'This is an updated anoymous object'} |
| created     | 7 minutes ago                                  |
| lastUpdated | just now                                       |
+-------------+------------------------------------------------+
```

To close the loop, it is possible to search for metadata records by name. This
makes using the metadata service as a simple key-value store much more
tractable than is the default case for the metadata service.

```shell
# Return the overview view
$ tapis metadata search --name eq vaughn.d021c9f2e90369e3.191010T173722Z
+-----------------------------+--------+-----------------------------+-----------------------------+
| uuid                        | owner  | name                        | lastUpdated                 |
+-----------------------------+--------+-----------------------------+-----------------------------+
| 7095279578129362455-242ac11 | vaughn | vaughn.d021c9f2e90369e3.191 | 2019-10-10T12:44:40.125-05: |
| a-0001-012                  |        | 010T173722Z                 | 00                          |
+-----------------------------+--------+-----------------------------+-----------------------------+

# Return the JSON record view
$ tapis metadata search --name eq vaughn.d021c9f2e90369e3.191010T173722Z -v
[
  {
    "uuid": "7095279578129362455-242ac11a-0001-012",
    "owner": "vaughn",
    "associationIds": [],
    "name": "vaughn.d021c9f2e90369e3.191010T173722Z",
    "value": {
      "info": "This is an updated anoymous object"
    },
    "created": "2019-10-10T12:37:22.269-05:00",
    "lastUpdated": "2019-10-10T12:44:40.125-05:00",
    "_links": {
      "self": {
        "href": "https://api.sd2e.org/meta/v2/data/7095279578129362455-242ac11a-0001-012"
      },
      "permissions": {
        "href": "https://api.sd2e.org/meta/v2/data/7095279578129362455-242ac11a-0001-012/pems"
      },
      "owner": {
        "href": "https://api.sd2e.org/profiles/v2/vaughn"
      },
      "associationIds": []
    }
  }
]
```

27-09-2019 | No changes

20-09-2019 | Metadata search and list are implemented. Creation and update of metadata
records is not implemented, nor are permissions or metadata JSON schemas.

## Profiles

18-10-2019 | Profiles search is now available. Only one attribute can be
queried at a time and only the equality **eq** modifier is supported due to
limitations of the profiles service.

27-09-2019 | No changes

20-09-2019 | Viewing of another user's profile as well as that of the currently logged-in
user is supported. List and search are not implemented at present.

## Notifications

27-09-2019 | No changes

20-09-2019 | No notifications commands are ready to test

## Postits

27-09-2019 | No changes

20-09-2019 | No postits commands are ready to test

