# Local System Setup

UnifyBio supports use in a multitude of configurations, from individual laptops to
on-premise systems in labs and organizations and large, distributed cloud systems.
For both dev convenience, and to enable individual scientists and small teams,
UnifyBio provides two local system configuration options.

## Local System Management with Docker Compose

By convention, software distributions that contain UnifyBio tools ship
with a local docker compose system that consists of:

- a [Postgres database](https://www.postgresql.org/), which acts as Datomic's underlying storage.
- a [Datomic transactor](https://docs.datomic.com/peer-tutorial/transactor.html)
- a [Query Service](https://github.com/vendekagon-labs/datomic-query-service),
  with a JSON Query API that backs the R and Python libraries

Local systems write high dimensional measurement data to
file storage instead of cloud object storage, so
measurement matrices and HDF, parquet, and zarr files will be stored
in a subdirectory and accessed from there (this configuration can be overwritten).

To use the local docker compose system, you will need to install
[Docker Desktop](https://docs.docker.com/desktop/) or the
[Docker Engine](https://docs.docker.com/engine/),
depending on your platform.

After obtaining a UnifyBio software distribution, you can run:

```
bin/start-local-system
```

To start a local system. _Note_: while this script is typically provided as a convenience,
all that is strictly necessary is to navigate to the directory which contains the
`docker-compose.yml` file and run `docker-compose up`.


## Local System Management through JVM process management

While containerization provides user convenience, it also results in operational
complexity that is not strictly necessary for use.
UnifyBio is tested and supports use with JVM 21+ conforming
distributions of
[temurin](https://adoptium.net/temurin/releases/),
[corretto](https://aws.amazon.com/corretto/?filtered-posts.sort-by=item.additionalFields.createdDate&filtered-posts.sort-order=desc), and
[Oracle Java](https://www.oracle.com/java/technologies/downloads/). You can run any
of the individual components of the local Unify system as components on the same
machine, or distributed across several machines in any suitable network configuration.

While UnifyBio's core tools are written in Clojure, they are distributed
as uberjars and you will not need a Clojure distribution unless you
intend to do development, in which case you should refer to Clojure's official
[installation](https://clojure.org/guides/install_clojure) and 
[getting started](https://clojure.org/guides/getting_started) guides.
