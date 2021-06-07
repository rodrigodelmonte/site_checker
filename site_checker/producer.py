import datetime
import json
import logging
import re
from dataclasses import asdict, dataclass

from clients import http_client
from clients.kafka_client import KafkaClient
from configs import KafkaConfig, WebsiteConfig
from kafka.errors import KafkaError, KafkaTimeoutError
from requests.models import Response


@dataclass
class WebsiteMetrics:
    url: str
    regex: str
    has_regex: bool
    status_code: int = 0
    response_time: int = 0
    ocurred_at: str = ""


class Producer(KafkaClient):
    def __init__(self, kafka_config: KafkaConfig) -> None:
        super().__init__(kafka_config)
        self.logger = logging.getLogger(__name__)

    def _get_response_time(self, response: Response) -> int:
        time_elapsed = response.elapsed.total_seconds()
        response_time: int = int(round(time_elapsed * 1000, 3))

        return response_time

    def _check_regex(self, regex: str, content: str) -> bool:
        has_regex: bool = bool(re.search(regex, content))

        return has_regex

    def _get_metrics(self, website: WebsiteConfig) -> str:

        self.logger.info(f"Getting metrics from url {website.url}")

        metrics = WebsiteMetrics(url=website.url, regex=website.regex, has_regex=False)
        response = http_client.get_response(website.url)
        metrics.status_code = response.status_code
        metrics.response_time = self._get_response_time(response)
        metrics.ocurred_at = datetime.datetime.utcnow().isoformat()

        if metrics.regex and metrics.status_code == 200:
            metrics.has_regex = self._check_regex(website.regex, response.text)

        website_metrics = json.dumps(asdict(metrics))

        self.logger.debug(f"Metrics collected: {website_metrics}")

        return website_metrics

    def _publish_metrics(self, website: WebsiteConfig, metrics: str) -> None:

        self.logger.info(f"Publishing metrics from url {website.url}")

        try:
            self.producer().send(website.name, value=metrics)
            self.producer().flush()
        # Kafka handling errors example:
        # https://www.programcreek.com/python/example/92970/kafka.errors.KafkaError
        except KafkaTimeoutError as e:
            self.logger.exception(f"Kafka Producer Timeout Error:\n{e}")
        except KafkaError as e:
            self.logger.exception(f"Kafka Error occurred:\n{e}")

    def check_website(self, website: WebsiteConfig) -> None:

        metrics = self._get_metrics(website)
        if metrics:
            self._publish_metrics(website, metrics)
