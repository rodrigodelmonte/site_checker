# site_checker
![Python Version](https://img.shields.io/badge/Python-3.7-blue)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Overview

`site_checker` monitors website availability over the
network, produces metrics about this and passes these events through `Kafka` instance into `PostgreSQL` database.
`site_checker` is divided in two components:

- **producer:** collect website metrics and publish results to `Kafka`
- **consumer:** consume metrics from `Kafka` topics and save metrics into an `PostgreSQL` database.

![architecture diagram](docs/site_checker_architecture.png)

## Contribute
For more detail, please check [CONTRIBUTING.md](CONTRIBUTING.md) guide.
