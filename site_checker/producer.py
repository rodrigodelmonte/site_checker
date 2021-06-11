import datetime
import json
import logging
import re
from dataclasses import asdict

from clients.http_client import get_response
from clients.kafka_client import KafkaClient
from configs import KafkaConfig, WebsiteConfig
from models import WebsiteMetrics
from requests.models import Response


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

    def _get_metrics(self, website: WebsiteConfig) -> WebsiteMetrics:

        self.logger.info(f"Getting metrics from website {website.name}")

        metrics = WebsiteMetrics(
            name=website.name, url=website.url, regex=website.regex, has_regex=False
        )
        response = get_response(website.url)
        if response:
            metrics.status_code = response.status_code
            metrics.response_time = self._get_response_time(response)
            metrics.ocurred_at = datetime.datetime.utcnow().isoformat()

            if metrics.regex and metrics.status_code == 200:
                metrics.has_regex = self._check_regex(website.regex, response.text)

            self.logger.debug(f"Metrics collected: {metrics}")

        return metrics

    def _publish_metrics(self, website: WebsiteConfig, metrics: str) -> None:

        self.logger.info(f"Publishing metrics from website {website.name}")

        self.producer().send(website.name, value=metrics)
        self.producer().flush()

    def check_website(self, website: WebsiteConfig) -> None:

        metrics = self._get_metrics(website)
        if metrics.status_code:
            website_metrics = json.dumps(asdict(metrics))
            self._publish_metrics(website, website_metrics)
