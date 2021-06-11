import logging
from typing import Optional

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.models import Response
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def get_response(url: str) -> Optional[Response]:
    """Receives an url string and returns a request.Response object.
    It uses timeout and retry logic to avoid errors due to network and servers instability

    Args:
        url (str): String example: http://www.python.org

    Returns:
        Response: Response object
    """

    # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
    response = None
    session = Session()
    connect_timeout = 2
    read_timeout = 5

    retry_strategy = Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, timeout=(connect_timeout, read_timeout))
    except ConnectionError as e:
        logger.exception(f"HTTP Connection Error occurred:\n{e}")

    return response
