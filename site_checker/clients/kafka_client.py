import json
from functools import lru_cache

from configs import KafkaConfig
from kafka import KafkaProducer


class KafkaClient:
    def __init__(self, kafka_config: KafkaConfig):

        self.kafka_config = kafka_config

    @lru_cache()
    def producer(self) -> KafkaProducer:
        """Configure a KafkaProducer using `KafkaConfig`
        The decorator @lru_cache() the  make sure the SSL files are read just once in the
        first execution. The post executions uses a cached object in memory.

        Returns:
            KafkaProducer: A Kafka client that publishes records to the Kafka cluster.
        """
        return KafkaProducer(
            bootstrap_servers=self.kafka_config.bootstrap_servers,
            security_protocol=self.kafka_config.security_protocol,
            ssl_cafile=self.kafka_config.ssl_cafile,
            ssl_certfile=self.kafka_config.ssl_certfile,
            ssl_keyfile=self.kafka_config.ssl_keyfile,
            retries=3,
            retry_backoff_ms=1000,
            value_serializer=lambda v: json.dumps(v).encode("ascii"),
        )
