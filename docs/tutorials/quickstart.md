# Quickstart

This section contains step-by-step instructions to import the template dataset, an example dataset constructed from multiple
public data sources that exercises a large surface area of Unify's import functionality. Running these steps will help you
make sure that everything is set up correctly on your system and also provide an overall view of the process.

## Setup

This quickstart assumes you have a local UnifyBio distribution downloaded, such as 
the one provided by the Rare Cancer Research Foundation (RCRF)'s Pattern Data Commons.
At present, UnifyBio is in an early alpha phase and only available in packaged
form to RCRF's research partners. To get access to the Pattern distribution,
you will need to contact [RCRF](https://rarecancer.org/initiatives).

### Local System via Docker Compose

To use the provided local system, you need to [install Docker](https://docs.docker.com/)
and ensure you can stand up a local system with Docker Compose. You will also need a JVM
(version 21 or later required). You might already have one available,
which you can check by running:

```
java -version
```

in a terminal. If you do not have a JVM installed, [Temurin 21 or 22](https://adoptium.net/installation/)
is a good default.

#### Additional configuration

The current Pattern distribution requires hostname remapping at the OS level
to ensure the Unify CLI's peer process can communicate with the other system
components using the same configuration. Edit your `/etc/hosts` file and
add these two entries:

```python title="/etc/hosts" hl_lines="2-3"
127.0.0.1	localhost
127.0.0.1	transactor
127.0.0.1	postgres
```

#### Starting the local system

Download and unzip your UnifyBio distribution. If you have not been provided one, you can use
the Pattern distribution provided by [RCRF](https://rarecancer.org/initiatives).

- Navigate to the directory created when you unzip or clone the UnifyBio distribution.
- Start a local system with:

    ```
    bin/start-local-system
    ```

All subsequent commands assume you are in the UnifyBio distribution directory and have a local system
running with Docker compose.

## Simple Import Workflow

This quickstart shows an example of working with a minimal import, using the Unify CLI and
the template dataset. The Pattern distribution contains a copy of the template-dataset in the `template-dataset/`
subdirectory. You can also browse the copy used in Unify's test systems
[here](https://github.com/vendekagon-labs/unify/tree/main/test/resources/systems/candel/template-dataset).


### Prepare

The first thing you will do is transform data from tables into entity map representations in _edn_ form,
by using the Unify CLI prepare task.

```
bin/unify prepare --import-config $PATH-TO-TEMPLATE-DATASET/config.yaml --working-directory PATH-TO-TEMP-DIRECTORY
```

When prepare has completed successfully, you will be able to transact the data into a database.

### Request Database

Before we can transact data, we need a database to transact it into. For this quickstart, we'll
request a dev database from the local UnifyBio system:

```
bin/unify request-db --database YOUR-DB-NAME
```

This will create a new Datomic database in your local system. In most UnifyBio workflows,
you will work iteratively with dev databases to create, debug, and update the dataset
import.

_Note_: Local dev databases are suitable for learning Unify, but it is expected that
production ready datasets will be published or otherwise blessed for use
in a centralized system through an org specified process.

### Transact

Now that we have prepared a dataset for import and have a database to import it into, we
are ready to run `transact`. Note that `YOUR-DB-NAME` is the same `--database` you
created in the request step.

```
bin/unify transact --database YOUR-DB-NAME --working-directory PATH-TO-TEMP-DIRECTORY
```
The data is now in the database and can be queried, accessed through integrations,
and validated.

### Validate

UnifyBio distributions include a `validate` task, which ensures that data in a database
conforms to org provided specifications. These ensure data are structurally and
semantically sound, as well as referentially consistent (all targets of entity reference
attributes refer to other entities that actually exist).

Validate your import with this command:

```
bin/validate --database YOUR-DB-NAME --dataset "template-dataset"
```

## Query Your Data

You can now run queries against the local database! If you are using the Pattern Data Commons distribution and schema,
you can install the `patternq` [Python](https://github.com/rcrf/patternq) or [R](https://github.com/CANDELbio/wick) libraries
for free form query.

The Pattern distribution contains an example query you can run with Python. This
script accesses data through the Query service included in the local docker compose system.
You will need to have the `requests` package in your local Python environment to run it.

```
python util/local-test-query.py YOUR-DB-NAME
```

You can optionally include a second arg to `local-test-query.py` that contains a file path to
a JSON file containing a query request body.
While covering the possible contents and [query language](https://docs.datomic.com/query/query-data-reference.html)
are outside the scope of
this tutorial, you can inspect the contents of the Python script, consult some of the
[examples](https://github.com/vendekagon-labs/datomic-query-service/blob/main/resources/example-q.json)
in the query service repo, and use the
[live schema browser](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/index.html)
as guides for constructing more advanced queries.

