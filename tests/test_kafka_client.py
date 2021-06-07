from site_checker.clients.kafka_client import KafkaClient


def test_kafka_client(config_path):

    kafka_client = KafkaClient(config_path)
    assert hasattr(kafka_client, "kafka_config")
