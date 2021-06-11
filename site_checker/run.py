#!/usr/bin/env python
import logging
import signal
import sys
import time

import click
import configs
from clients.postgres_client import PostgresClient
from consumer import Consumer
from producer import Producer


def exit_gracefully(signalNumber, frame):
    logger.info(f"Received Signal: {signalNumber}, Stopping worker.")
    sys.exit(0)


signal.signal(signal.SIGTERM, exit_gracefully)

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger = logging.getLogger("site_checker")


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--config-path",
    help="Path to configuration file `config.ini`. When used the others params are not required",
)
@click.option(
    "--kafka-bootstrap-servers", help="Kafka bootstrap server URI, e.g: <host>:<port>"
)
@click.option(
    "--kafka-security-protocol", help="Kafka Security Protocol, e.g: SSL", default="SSL"
)
@click.option("--kafka-ssl-cafile", help="Kafka path to ssl CA file, e.g: ./ca.pem")
@click.option(
    "--kafka-ssl-certfile", help="Kafka path to ssl cert file, e.g: ./service.cert"
)
@click.option(
    "--kafka-ssl-keyfile", help="Kafka path to ssl key file, e.g: ./service.key"
)
@click.option("--kafka-topic", help="Kafka topic to consume")
@click.option("--postgres-user", help="Postgres database user")
@click.option("--postgres-password", help="Postgres database password")
@click.option("--postgres-host", help="Postgres database hostname")
@click.option("--postgres-port", help="Postgres database port")
@click.option("--postgres-database", help="Postgres database name")
@click.option(
    "--postgres-sslmode", help="Postgres database SSL mode", default="verify-ca"
)
@click.option("--postgres-sslrootcert", help="Postgres database SSL root cert path")
@click.option(
    "--dry-run", help="DRY-RUN mode, command will not check websites", is_flag=True
)
def consumer(
    config_path,
    kafka_bootstrap_servers,
    kafka_security_protocol,
    kafka_ssl_cafile,
    kafka_ssl_certfile,
    kafka_ssl_keyfile,
    kafka_topic,
    postgres_user,
    postgres_password,
    postgres_host,
    postgres_port,
    postgres_database,
    postgres_sslmode,
    postgres_sslrootcert,
    dry_run,
):
    """Consume kafka topic and writes records in a Postgres database table"""

    if config_path:
        logger.info("Starting site_checker Consumer.")
        logger.info(f"Reading configuration file {config_path}.")

        kafka_config = configs.kafka_config(config_path)
        kafka_topics = configs.kafka_topics(config_path)

        postgres_config = configs.postgres_config(config_path)

        if dry_run:
            sys.exit(0)

        postgres_client = PostgresClient()
        postgres_connection_pool = postgres_client.create_connection_pool(
            postgres_config
        )

        consumer = Consumer(kafka_config, kafka_topics, postgres_connection_pool)
        consumer.subscribe_topics()

    else:
        logger.info("Starting site_checker Consumer.")

        kafka_config = configs.KafkaConfig(
            bootstrap_servers=kafka_bootstrap_servers,
            security_protocol=kafka_security_protocol,
            ssl_cafile=kafka_ssl_cafile,
            ssl_certfile=kafka_ssl_certfile,
            ssl_keyfile=kafka_ssl_keyfile,
        )

        postgres_config = configs.PostgresConfig(
            user=postgres_user,
            password=postgres_password,
            host=postgres_host,
            port=postgres_port,
            database=postgres_database,
            sslmode=postgres_sslmode,
            sslrootcert=postgres_sslrootcert,
            min_connection=1,
            max_connection=2,
        )

        if dry_run:
            sys.exit(0)

        kafka_topics = []
        kafka_topics.append(kafka_topic)

        postgres_client = PostgresClient()
        postgres_connection_pool = postgres_client.create_connection_pool(
            postgres_config
        )

        consumer = Consumer(kafka_config, kafka_topics, postgres_connection_pool)
        consumer.subscribe_topics()


@click.command()
@click.option(
    "--config-path",
    help="Path to configuration file `config.ini`. When used the others params are not required",
)
@click.option("--name", help="Website name, e.g: python, cncf, apache")
@click.option("--url", help="Website URL to check, e.g: https://python.org/")
@click.option(
    "--regex", help="Verifies if the response contains the given regex pattern"
)
@click.option(
    "--kafka-bootstrap-servers", help="Bootstrap server URI, e.g: <host>:<port>"
)
@click.option(
    "--kafka-security-protocol", help="Security Protocol, e.g: SSL", default="SSL"
)
@click.option("--kafka-ssl-cafile", help="Path to ssl CA file, e.g: ./ca.pem")
@click.option("--kafka-ssl-certfile", help="Path to ssl cert file, e.g: ./service.cert")
@click.option("--kafka-ssl-keyfile", help="Path to ssl key file, e.g: ./service.key")
@click.option(
    "--pooling-interval", help="The pooling check interval in SECONDS, e.g: 60"
)
@click.option(
    "--dry-run", help="DRY-RUN mode, command will not check websites", is_flag=True
)
def producer(
    name,
    url,
    regex,
    config_path,
    kafka_bootstrap_servers,
    kafka_security_protocol,
    kafka_ssl_cafile,
    kafka_ssl_certfile,
    kafka_ssl_keyfile,
    pooling_interval,
    dry_run,
):
    """
    Collects website metrics and publishes results to a Kafka topic.

    Metrics: status_code, response_time, has_regex

    """
    if config_path:
        logger.info("Starting site_checker Producer.")
        logger.info(f"Reading configuration file {config_path}.")
        websites = configs.websites_configs(config_path)
        logger.info(
            f"List of websites to check: {[website.name for website in websites]}"
        )
        logger.info(
            f"Default pooling interval {configs.POOLING_INTERVAL_IN_SECONDS} seconds."
        )

        producer = Producer(configs.kafka_config(config_path))

        if dry_run:
            sys.exit(0)

        while True:
            for website in websites:
                producer.check_website(website)
            time.sleep(configs.POOLING_INTERVAL_IN_SECONDS)
    else:
        logger.info("Starting site_checker producer")
        logger.info(f"Website to check {name.upper()} at url {url}")
        logger.info(f"Pooling interval {pooling_interval} seconds.")

        kafka_config = configs.KafkaConfig(
            bootstrap_servers=kafka_bootstrap_servers,
            security_protocol=kafka_security_protocol,
            ssl_cafile=kafka_ssl_cafile,
            ssl_certfile=kafka_ssl_certfile,
            ssl_keyfile=kafka_ssl_keyfile,
        )

        producer = Producer(kafka_config)

        website = configs.WebsiteConfig(name=name, url=url, regex=regex)

        if dry_run:
            sys.exit(0)

        while True:
            producer.check_website(website)
            time.sleep(int(pooling_interval))


cli.add_command(consumer)
cli.add_command(producer)

if __name__ == "__main__":
    cli()
