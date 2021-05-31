import datetime
import json
import re
from dataclasses import asdict, dataclass

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.packages.urllib3.util.retry import Retry

# https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
session = requests.Session()
retry_strategy = Retry(
    total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)


@dataclass
class HTTPResult:
    url: str
    regex: str
    has_regex: bool
    status_code: int = 0
    response_time: int = 0
    ocurred_at: str = ""


class HTTPClient:
    def __init__(self, url: str = "", regex: str = ""):
        self.url = url
        self.regex = regex
        self.result = HTTPResult(url=self.url, regex=self.regex, has_regex=False)

    def _get_response_time(self, response: Response) -> int:
        time_elapsed = response.elapsed.total_seconds()
        response_time: int = int(round(time_elapsed * 1000, 3))

        return response_time

    def _check_regex(self, regex: str, content: str) -> bool:
        has_regex: bool = bool(re.search(regex, content))

        return has_regex

    def check_url(self) -> str:
        try:
            response = session.get(self.url)
            self.result.status_code = response.status_code
            self.result.response_time = self._get_response_time(response)
            self.result.ocurred_at = datetime.datetime.utcnow().isoformat()
            if self.regex and self.result.status_code == 200:
                self.result.has_regex = self._check_regex(self.regex, response.text)
        except ConnectionError as e:
            print(e)

        return json.dumps(asdict(self.result))


# if __name__ == "__main__":
#     http_client = HTTPClient(url="https://python.org/ddd", regex="test")
#     result1: str = http_client.check_url()
#     print(result1)
#     http_client = HTTPClient(url="https://aiven.io/", regex="aiven")
#     result2: str = http_client.check_url()
#     print(result2)
