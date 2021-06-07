from unittest.mock import MagicMock, Mock

from site_checker.configs import WebsiteConfig
from site_checker.producer import Producer


def test_producer(kafka_config_fixture):

    producer = Producer(kafka_config_fixture)
    assert hasattr(producer, "kafka_config")
    assert hasattr(producer, "logger")


def test_producer_check_website(kafka_config_fixture):

    website = WebsiteConfig(name="test", url="http://test.com")
    metrics = {"name": "test", "url": "http://test.com", "status_code": "200"}

    producer = Producer(kafka_config_fixture)

    producer._get_metrics = MagicMock(return_value=metrics)
    producer._publish_metrics = Mock()

    producer.check_website(website)

    producer._get_metrics.assert_called_once_with(website)
    producer._publish_metrics.assert_called_once_with(website, metrics)
