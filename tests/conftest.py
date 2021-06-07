import pytest

from site_checker.configs import KafkaConfig, kafka_config


@pytest.fixture
def config_path():
    return "./example/example.config.ini"


@pytest.fixture
def kafka_config_fixture() -> KafkaConfig:
    return kafka_config("./example/config.ini")
