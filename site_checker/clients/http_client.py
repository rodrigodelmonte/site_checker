import logging

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.models import Response
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def get_response(url: str) -> Response:
    """Receives an url string and returns a request.Response object.
    It uses timeout and retry logic to avoid errors due to network and servers instability

    Args:
        url (str): String example: http://www.python.org

    Returns:
        Response: Response object
    """

    # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
    session = requests.Session()
    retry_strategy = Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, timeout=(2, 5))
    except ConnectionError as e:
        logger.exception(f"HTTP Connection Error occurred:\n{e}")

    return response
