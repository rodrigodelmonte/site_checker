from dataclasses import dataclass

from models import WebsiteMetrics

from site_checker.consumer import Consumer


@dataclass
class ValueFake:
    value: str = '{"name": "python", "url": "http://python.org/", "regex":"test", "has_regex":"True", "status_code":200, "response_time":"153", "ocurred_at":"2021-06-13T19:35:17.233908"}'  # noqa: E501


class ConsumerFake:
    def __init__(self):
        self.value = ValueFake()
        self.stop = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.stop:
            raise StopIteration
        self.stop = True
        return self.value

    def subscribe(self, topics):
        pass


def test_consumer_subscribe_topics(mocker, monkeypatch, kafka_config_fixture):

    # G
    PostgresClient = mocker.MagicMock()
    PostgresClient._execute_query = mocker.MagicMock()
    postgres_connection_pool = mocker.MagicMock()
    postgres_connection_pool.connection.autocommit = mocker.MagicMock(return_value=True)
    postgres_connection_pool.getconn = mocker.MagicMock(
        return_value=postgres_connection_pool.connection.autocommi
    )
    postgres_connection_pool.putconn = mocker.MagicMock(return_value=None)
    postgres_connection_pool.autocommit = mocker.MagicMock(return_value=True)

    consumer_test = Consumer(kafka_config_fixture, ["python"], postgres_connection_pool)

    def consumer_mock(self):
        comsumer_fake = ConsumerFake()
        return comsumer_fake

    monkeypatch.setattr(Consumer, "consumer", consumer_mock)

    comsumer_fake = ConsumerFake()
    expected = [record for record in comsumer_fake]

    # W
    mocker.spy(consumer_test, "_proccess_metrics")
    mocker.spy(consumer_test, "_save_metrics")

    consumer_test.subscribe_topics()

    # T
    consumer_test._proccess_metrics.assert_called_with(expected[0])

    website_metrics = WebsiteMetrics(
        name="python",
        url="http://python.org/",
        regex="test",
        has_regex="True",
        status_code=200,
        response_time="153",
        ocurred_at="2021-06-13T19:35:17.233908",
    )

    consumer_test._save_metrics.assert_called_with(website_metrics)
