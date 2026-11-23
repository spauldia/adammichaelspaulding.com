"""Downloads the public profile JSON."""

import json
from urllib.request import urlopen

from app.constants import PROFILE_TIMEOUT_SECONDS


def fetch_profile_json(url: str) -> str:
    """Return the profile JSON text.

    Raises:
        ValueError: The response is not valid JSON.
    """
    with urlopen(url, timeout=PROFILE_TIMEOUT_SECONDS) as response:
        text = response.read().decode("utf-8")
    json.loads(text)
    return text
