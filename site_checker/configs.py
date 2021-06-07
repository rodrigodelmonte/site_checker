import configparser
from dataclasses import dataclass
from typing import List

POOLING_INTERVAL_IN_SECONDS = 20


@dataclass
class WebsiteConfig:
    name: str
    url: str = ""
    regex: str = ""


def websites_configs(config_path: str) -> List[WebsiteConfig]:
    """Read configuration from config.ini file and returns
    websites configurations to be used by the producer to collect
    website metrics.

    Example:
        [
            WebsiteConfig(
                name=name,
                url=url,
                regex=regex,
            )
        ]

    Args:
        config_path (str): The path for the config.ini file.

    Returns:
        List[WebsiteConfig]: object with websites configurations
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    websites = [c for c in config.sections() if c.startswith("website_")]

    websites_configs = []
    for website in websites:
        web: WebsiteConfig = WebsiteConfig(
            name=website.replace("website_", ""),
            url=config[website].get("url", ""),
            regex=config[website].get("regex", ""),
        )
        websites_configs.append(web)

    return websites_configs


@dataclass
class KafkaConfig:
    bootstrap_servers: str
    security_protocol: str
    ssl_cafile: str
    ssl_certfile: str
    ssl_keyfile: str


def kafka_config(config_path: str) -> KafkaConfig:
    """Read configuration from config.ini file and returns a
    KafkaConfig object to be used by the kafka client.

    Args:
        config_path (str): The path for the config.ini file.

    Returns:
        KafkaConfig: object with kafka configurations
    """

    config = configparser.ConfigParser()
    config.read(config_path)

    return KafkaConfig(
        bootstrap_servers=config["kafka"].get("bootstrap_servers", ""),
        security_protocol=config["kafka"].get("security_protocol", "SSL"),
        ssl_cafile=config["kafka"].get("ssl_cafile", "./ca.pem"),
        ssl_certfile=config["kafka"].get("ssl_certfile", "./service.cert"),
        ssl_keyfile=config["kafka"].get("ssl_keyfile", "./service.key"),
    )
