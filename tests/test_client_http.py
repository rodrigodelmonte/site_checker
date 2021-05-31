from typing import Dict

import pytest
from checker import HTTPClient


@pytest.mark.parametrize(
    "url, regex, mock_check_url",
    [
        ["https://python.org", "legal", {"status_code": 200, "has_regex": True}],
        ["https://python.org", "ABC123", {"status_code": 200, "has_regex": False}],
        ["https://github.com/", "", {"status_code": 200, "has_regex": False}],
        [
            "https://github.com/doesnotexitsts",
            "",
            {"status_code": 404, "has_regex": False},
        ],
    ],
)
def test_check_url(monkeypatch, url, regex, mock_check_url):
    def _mock_check_url(payload) -> Dict:
        return mock_check_url

    monkeypatch.setattr(HTTPClient, "check_url", _mock_check_url)

    http_client = HTTPClient(url=url, regex=regex)
    result: Dict = http_client.check_url()

    assert result["status_code"] == mock_check_url["status_code"]
    assert result["has_regex"] == mock_check_url["has_regex"]
