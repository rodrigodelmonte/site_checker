# site_checker
![Python Version](https://img.shields.io/badge/Python-3.7-blue)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Overview

`site_checker` monitors website availability over the
network, produces metrics about this and passes these events through `Kafka` instance into `PostgreSQL` database.
`site_checker` is divided into two components:

- **producer:** collect website metrics and publish results to `Kafka`
- **consumer:** consume metrics from `Kafka` topics and save metrics into a `PostgreSQL` database.

![architecture diagram](docs/site_checker_architecture.png)

## Demo

[![asciicast](https://asciinema.org/a/3zKRgfBovD0qMehdVwWBuf0ao.svg)](https://asciinema.org/a/3zKRgfBovD0qMehdVwWBuf0ao)

## Getting Started

This section will guide you through the steps to reproduce locally the demo presented above.

This tutorial expects you have already a `Kafka` and `Postgres` instance running. For more details please check, [How to set up managed Apache Kafka](https://www.youtube.com/watch?v=YH-S3Huwfms) and [How to deploy an open source database](https://www.youtube.com/watch?v=t95IQ0kpbFY).

1. Checkout this repository:

```sh
$ git clone git@github.com:aiven-recruitment/SRE-20210601-rodrigodelmonte.git
$ cd SRE-20210601-rodrigodelmonte
```

2. Setup credentials

```sh
$ vim example/example.consumer.env # replace <CHANGEME> entries
$ vim example/example.producer.env # replace <CHANGEME> entries
# Copy the Kafka and Postgres SSL certificates to example/ folder
$  cp ~/Downloads/ca.pem example/
$  cp ~/Downloads/service.* example/
```

3. Start docker-compose

```sh
$ make run
```

4. Check application logs.

```sh
$ make logs
```

5. Check the data saved into `Postgres`.

 ```sql
$ psql -U <USER> -h <HOSTNAME> -p <PORT> defaultdb
$ select * from site_checker.apache;
 ```

6. Clean

```sh
$ make clean
```
## Contribute
For more detail, please check [CONTRIBUTING.md](CONTRIBUTING.md) guide.
