import json
from dataclasses import asdict

from pytest import mark

from site_checker.clients import http_client
from site_checker.configs import WebsiteConfig
from site_checker.models import WebsiteMetrics
from site_checker.producer import Producer


def test_producer(kafka_config_fixture):

    producer = Producer(kafka_config_fixture)
    assert hasattr(producer, "kafka_config")
    assert hasattr(producer, "logger")


def test_producer_check_website_flow(mocker, monkeypatch, kafka_config_fixture):

    # G
    producer = Producer(kafka_config_fixture)
    website = WebsiteConfig(name="test-mocked", url="http://test.com")
    metrics = WebsiteMetrics(
        name="test-mocked",
        url="http://test.com",
        regex="",
        has_regex=False,
        status_code=200,
        response_time=107,
        ocurred_at="",
    )
    website_metrics = json.dumps(asdict(metrics))

    # W
    def _get_metrics_mock(website) -> str:
        return metrics

    def _publish_metrics_mock(website, metrics) -> None:
        return None

    monkeypatch.setattr(producer, "_get_metrics", _get_metrics_mock)
    monkeypatch.setattr(producer, "_publish_metrics", _publish_metrics_mock)

    mocker.spy(producer, "_get_metrics")
    mocker.spy(producer, "_publish_metrics")

    producer.check_website(website)

    # T
    producer._get_metrics.assert_called_with(website)
    producer._publish_metrics.assert_called_with(website, website_metrics)


def test_producer_get_response_time_return_int(mocker, producer_fixture):

    # G
    response = mocker.MagicMock()
    response.elapsed.total_seconds = mocker.MagicMock(return_value=0.10794)

    producer = producer_fixture

    # W
    response_time = producer._get_response_time(response)

    # T
    assert response_time == 107


@mark.parametrize(
    "regex, content, expected",
    [
        ["Py.{4}", "Python is faster than ...", True],
        ["Py.{4}", "It doesn't have enough memory to run this Java application", False],
    ],
)
def test_producer_check_regex_return_bool(producer_fixture, regex, content, expected):

    # G
    producer = producer_fixture

    # W
    result = producer._check_regex(regex, content)

    # T
    assert result == expected


@mark.skip(reason="Mock strategy doesn't work yet")
def test_producer_get_metrics_error_code_returned(
    producer_fixture, monkeypatch, mocker
):
    # G
    producer = producer_fixture
    website = WebsiteConfig(name="unkwown", url="http://doesnotexists.io")

    def get_response_mock():
        response = mocker.MagicMock()
        response.status_code = 200
        return response

    monkeypatch.setattr(http_client, "get_response", get_response_mock)

    # W
    website_metrics = producer._get_metrics(website)

    # T
    assert website_metrics.status_code == 404
