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

> 1.  Python 2.7.x is not supported (but will be)
> 2.  ~~No **files** commands are implemented~~
> 3.  No **actors** or **tacclab** commands are implemented
> 4.  The **watch** function from the old jobs-submit is gone and will
>     never return
> 5.  ~~Impersonation token issuance is not yet implemented~~
> 6.  The beloved `auth switch` is not yet implemented
> 7.  Metadata schema and record management commands are not yet
>     implemented
> 8.  No **notifications** commands are implemented
> 9.  The module is not yet available on PyPi
> 10. Documentation builds are broken
> 11. Creation of the Bash autocomplete config is broken
> 12. Search on dates is broken
> 12. Search on booleans can be broken (try `--boolean eq true`)
> 13. ~~Access tokens passed via `-z` or `--token` are not honored~~

## Installation

20-09-2019 | The CLI is installable from git checkout
  - It must be installable in **editable** mode (`pip install -e
    .`)
  - It must be installable in a virtual environment
  - It must be installable using setuptools (`python setup.py
    install`)
  - It must be installable under Python 3.5, 3.6, and 3.7
    (Python 2.7 support is forthcoming)

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

20-09-2019 |The CLI uses .env files and environment variables to configuring
some persistent settings. This will be described in more detail in
future testing sessions.

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

27-09-2019 | No changes

20-09-2019 | Feel free to exercise the entire *apps* lifecycle save for cloning. Creation,
updating, publishing, search & discovery, and sharing are all implemented.

## Jobs

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

04-10-2019 | File deletion is now supported. File history is now supported.

27-09-2017 | File listing, inspection, and downloads (including recursive) are
now implemented. File uploads are also working. Here is a sample list operation.

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

27-09-2019 | No changes

20-09-2019 | Core Tapis *systems* functions are implemented. Queue management is still missing as
is the ability to atomically update a system's login inforamation.

## Metadata

27-09-2019 | No changes

20-09-2019 | Metadata search and list are implemented. Creation and update of metadata
records is not implemented, nor are permissions or metadata JSON schemas.

## Profiles

27-09-2019 | No changes

20-09-2019 | Viewing of another user's profile as well as that of the currently logged-in
user is supported. List and search are not implemented at present.

## Notifications

27-09-2019 | No changes

20-09-2019 | No notifications commands are ready to test

## Postits

27-09-2019 | No changes

20-09-2019 | No postits commands are ready to test

