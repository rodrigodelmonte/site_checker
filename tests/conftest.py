import pytest

from site_checker.configs import kafka_config
from site_checker.producer import Producer


@pytest.fixture
def config_path():
    return "./example/example.config.ini"


@pytest.fixture
def kafka_config_fixture(config_path):
    return kafka_config(config_path)


@pytest.fixture
def producer_fixture(kafka_config_fixture):
    return Producer(kafka_config_fixture)
