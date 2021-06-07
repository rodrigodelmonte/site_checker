#!/usr/bin/env python
import logging
import signal
import sys
import time

import click
import configs
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
def consumer():
    pass


@click.command()
@click.option("--name", help="Website name, e.g: python, cncf, apache")
@click.option("--url", help="Website URL to check, e.g: https://python.org/")
@click.option("--regex", help="Regex string to check, i.e: about")
@click.option("--config-path", help="Path to configuration file `config.ini`")
@click.option(
    "--kafka-bootstrap-servers", help="Bootstrap server URI, e.g: <hott>:<port>"
)
@click.option(
    "--kafka-security-protocol", help="Security Protocal, e.g: SSL", default="SSL"
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
        logger.info(f"Websites to check {name.upper()} at url {url}")
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
