from dataclasses import dataclass


@dataclass
class WebsiteMetrics:
    name: str
    url: str
    regex: str
    has_regex: bool
    status_code: int = 0
    response_time: int = 0
    ocurred_at: str = ""
