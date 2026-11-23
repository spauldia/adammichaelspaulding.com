"""Limits how many questions one visitor can ask."""

import hashlib
import hmac
from datetime import datetime

from app.clients.dynamodb_client import TableClient
from app.constants import ONE_DAY_SECONDS, TEN_MINUTES_SECONDS

COUNT_ATTRIBUTE = "count"


class RateLimitService:
    """Counts questions per visitor in 10-minute and daily windows."""

    def __init__(self, table: TableClient, salt: str, per_10_min: int, per_day: int) -> None:
        self._table = table
        self._salt = salt.encode()
        self._per_10_min = per_10_min
        self._per_day = per_day

    def allow(self, client_ip: str, now: datetime) -> bool:
        """Count this question and return True when the visitor is under both limits."""
        visitor = self._visitor_id(client_ip)
        epoch = int(now.timestamp())
        window = epoch // TEN_MINUTES_SECONDS
        short_count = self._table.add_number(
            f"rate#{visitor}#10m#{window}", COUNT_ATTRIBUTE, 1, epoch + 2 * TEN_MINUTES_SECONDS
        )
        day_count = self._table.add_number(
            f"rate#{visitor}#day#{now:%Y-%m-%d}", COUNT_ATTRIBUTE, 1, epoch + 2 * ONE_DAY_SECONDS
        )
        return short_count <= self._per_10_min and day_count <= self._per_day

    def _visitor_id(self, client_ip: str) -> str:
        return hmac.new(self._salt, client_ip.encode(), hashlib.sha256).hexdigest()[:32]
