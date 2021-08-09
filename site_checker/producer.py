import datetime
import json
import logging
import re
from dataclasses import asdict

from clients import http_client
from clients.kafka_client import KafkaClient
from configs import KafkaConfig, WebsiteConfig
from models import WebsiteMetrics
from requests.models import Response


class Producer(KafkaClient):
    def __init__(self, kafka_config: KafkaConfig) -> None:
        super().__init__(kafka_config)
        self.logger = logging.getLogger(__name__)

    def _get_response_time(self, response: Response) -> int:
        """Returns the approximated response time in milliseconds
        The object `response.elapsed` measures the time in taken between
        sending the first byte of the request and finishing parsing the headers,
        it returns the time in microseconds. The total_seconds() method
        returns a float number.value
        Ref: https://docs.python-requests.org/en/master/api/#requests.Response.elapsed


        Args:
            response (Response): Website response object

        Returns:
            int: Respose time in Millisecond
        """

        time_elapsed = response.elapsed.total_seconds()
        response_time: int = int(round(time_elapsed * 1000, 3))

        return response_time

    def _check_regex(self, regex: str, content: str) -> bool:
        """Receives a regex + content, and returns a boolean

        Args:
            regex (str): regex to match
            content (str): content

        Returns:
            [boolean]: has_regex
        """

        has_regex: bool = bool(re.search(regex, content))

        return has_regex

    def _get_metrics(self, website: WebsiteConfig) -> WebsiteMetrics:
        """Get metrics from websites

        Args:
            website (WebsiteConfig): website to get metrics

        Returns:
            WebsiteMetrics: metrics
        """

        self.logger.info(f"Getting metrics from website {website.name}")

        metrics = WebsiteMetrics(
            name=website.name, url=website.url, regex=website.regex, has_regex=False
        )
        response = http_client.get_response(website.url)
        if response:
            metrics.status_code = response.status_code
            metrics.response_time = self._get_response_time(response)
            metrics.ocurred_at = datetime.datetime.utcnow().isoformat()

            if metrics.regex and metrics.status_code == 200:
                metrics.has_regex = self._check_regex(website.regex, response.text)

            self.logger.debug(f"Metrics collected: {metrics}")

        return metrics

    def _publish_metrics(self, website: WebsiteConfig, metrics: str) -> None:
        """Publish website metrics to Kafka cluster

        Args:
            website (WebsiteConfig): to retrieve the topic to be used.
            metrics (str): Website metrics to be published
        """

        self.logger.info(f"Publishing metrics from website {website.name}")
        topic = website.name
        self.producer().send(topic, value=metrics)
        self.producer().flush()

    def check_website(self, website: WebsiteConfig) -> None:

        metrics = self._get_metrics(website)
        if metrics.status_code:
            website_metrics = json.dumps(asdict(metrics))
            self._publish_metrics(website, website_metrics)
