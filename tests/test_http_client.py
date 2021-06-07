import pytest

from site_checker.clients.http_client import get_response


@pytest.mark.parametrize(
    "url, status_code",
    [
        ["https://python.org", 200],
        ["https://github.com/doesnotexitsts", 404],
    ],
)
def test_get_response(requests_mock, url, status_code):

    requests_mock.get(url, status_code=status_code)
    response = get_response(url)
    assert response.status_code == status_code
