import json
import logging
import sys
from functools import lru_cache

from configs import KafkaConfig
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable


class KafkaClient:
    def __init__(self, kafka_config: KafkaConfig):
        self.kafka_config = kafka_config
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=None)
    def producer(self) -> KafkaProducer:
        """Configure a KafkaProducer using `KafkaConfig`

        @lru_cache(maxsize=None) Simple lightweight unbounded function cache.
        Sometimes called “memoize”. @lru_cache(maxsize=None) is equal to @cache
        added to python version 3.9
        @lru_cache caches in memory the producer function, hence the SSL files are
        read only once.

        Returns:
            KafkaProducer: A Kafka client that publishes records to the Kafka cluster.
        """
        try:
            kafka_producer = KafkaProducer(
                bootstrap_servers=self.kafka_config.bootstrap_servers,
                security_protocol=self.kafka_config.security_protocol,
                ssl_cafile=self.kafka_config.ssl_cafile,
                ssl_certfile=self.kafka_config.ssl_certfile,
                ssl_keyfile=self.kafka_config.ssl_keyfile,
                retries=3,
                retry_backoff_ms=1000,
                value_serializer=lambda v: json.dumps(v).encode("ascii"),
            )
        except NoBrokersAvailable as e:
            self.logger.exception(f"Kafka Producer Error:\n{e}")
            sys.exit(1)

        return kafka_producer

    def consumer(self) -> KafkaConsumer:
        """Configure a KafkaConsumer using `KafkaConfig`

        Returns:
            KafkaConsumer: A Kafka client that consumes records from the Kafka cluster.
        """
        try:
            kafka_consumer = KafkaConsumer(
                bootstrap_servers=self.kafka_config.bootstrap_servers,
                security_protocol=self.kafka_config.security_protocol,
                ssl_cafile=self.kafka_config.ssl_cafile,
                ssl_certfile=self.kafka_config.ssl_certfile,
                ssl_keyfile=self.kafka_config.ssl_keyfile,
                value_deserializer=lambda v: json.loads(v.decode("ascii")),
            )
        except NoBrokersAvailable as e:
            self.logger.exception(f"Kafka Consumer Error:\n{e}")
            sys.exit(1)

        return kafka_consumer
