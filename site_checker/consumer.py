import json
import logging
from typing import List

from clients.kafka_client import KafkaClient
from clients.postgres_client import PostgresClient
from configs import KafkaConfig
from kafka.consumer.fetcher import ConsumerRecord
from models import WebsiteMetrics


class Consumer(KafkaClient):
    def __init__(
        self, kafka_config: KafkaConfig, kafka_topics: List, postgres_connection_pool
    ) -> None:
        super().__init__(kafka_config)
        self.kafka_topics = kafka_topics
        self.postgres_connection_pool = postgres_connection_pool
        self.postgres_client = PostgresClient()
        self.logger = logging.getLogger(__name__)

        for topic_name in kafka_topics:
            connection = postgres_connection_pool.getconn()
            self.postgres_client.create_table(connection, topic_name)
            postgres_connection_pool.putconn(connection)

    def _save_metrics(self, website_metrics: WebsiteMetrics) -> None:
        connection = self.postgres_connection_pool.getconn()
        self.postgres_client.insert(connection, website_metrics)
        self.logger.info(f"Metrics saved to database table: {website_metrics.name}")
        self.postgres_connection_pool.putconn(connection)

    def _proccess_metrics(self, record: ConsumerRecord) -> WebsiteMetrics:

        metrics = dict(json.loads((record.value)))
        website_metrics = WebsiteMetrics(**metrics)
        self.logger.info(f"Metrics consumed from Kafka topic: {website_metrics.name}")
        self.logger.debug(f"Website metrics processed: {website_metrics}")

        return website_metrics

    def subscribe_topics(self) -> None:

        consumer = self.consumer()
        consumer.subscribe(topics=self.kafka_topics)
        for record in consumer:
            website_metrics = self._proccess_metrics(record)
            self._save_metrics(website_metrics)
