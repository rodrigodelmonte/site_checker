import configparser
from dataclasses import dataclass
from typing import List


@dataclass
class WebsiteConfig:
    name: str
    url: str = ""
    regex: str = ""
    pooling_interval: int = 10


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
            pooling_interval=int(config[website].get("pooling_interval", "")),
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
    kfk_config = config["kafka"]

    return KafkaConfig(
        bootstrap_servers=kfk_config.get("bootstrap_servers", ""),
        security_protocol=kfk_config.get("security_protocol", "SSL"),
        ssl_cafile=kfk_config.get("ssl_cafile", "./ca.pem"),
        ssl_certfile=kfk_config.get("ssl_certfile", "./service.cert"),
        ssl_keyfile=kfk_config.get("ssl_keyfile", "./service.key"),
    )


def kafka_topics(config_path: str) -> List:
    """Read configuration from config.ini file and returns a
    list of kafka topics to be consumed.

    Args:
        config_path (str): The path for the config.ini file.

    Returns:
        List: of Kafka topics
    """

    config = configparser.ConfigParser()
    config.read(config_path)

    topics = []
    for c in config.sections():
        if c.startswith("website_"):
            topic = c.replace("website_", "")
            topics.append(topic)

    return topics


@dataclass
class PostgresConfig:
    user: str
    password: str
    host: str
    port: str
    database: str
    sslmode: str
    sslrootcert: str
    min_connection: int
    max_connection: int


def postgres_config(config_path: str) -> PostgresConfig:
    """Read configuration from config.ini file and returns a
    PostgresConfig object to be used by the postgres client.

    Args:
        config_path (str): The path for the config.ini file.

    Returns:
        PostgresConfig: object with postgres configurations
    """

    config = configparser.ConfigParser()
    config.read(config_path)
    pg_config = config["postgres"]

    return PostgresConfig(
        user=pg_config.get("user", ""),
        password=pg_config.get("password", ""),
        host=pg_config.get("host", ""),
        port=pg_config.get("port", "5432"),
        database=pg_config.get("database", "postgres"),
        sslmode=pg_config.get("sslmode", ""),
        sslrootcert=pg_config.get("sslrootcert", ""),
        min_connection=int(pg_config.get("min_connection", "1")),
        max_connection=int(pg_config.get("max_connection", "10")),
    )
