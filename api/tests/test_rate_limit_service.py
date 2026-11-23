from datetime import UTC, datetime, timedelta

from app.clients.dynamodb_client import TableClient
from app.services.rate_limit_service import RateLimitService

NOW = datetime(2026, 12, 5, 15, 30, tzinfo=UTC)


def test_allows_questions_up_to_the_10_minute_limit(table: TableClient) -> None:
    limiter = RateLimitService(table, salt="salt", per_10_min=3, per_day=30)

    results = [limiter.allow("203.0.113.7", NOW) for _ in range(4)]

    assert results == [True, True, True, False]


def test_new_10_minute_window_allows_more_questions(table: TableClient) -> None:
    limiter = RateLimitService(table, salt="salt", per_10_min=1, per_day=30)

    assert limiter.allow("203.0.113.7", NOW) is True
    assert limiter.allow("203.0.113.7", NOW) is False
    assert limiter.allow("203.0.113.7", NOW + timedelta(minutes=10)) is True


def test_daily_limit_applies_across_windows(table: TableClient) -> None:
    limiter = RateLimitService(table, salt="salt", per_10_min=10, per_day=2)

    assert limiter.allow("203.0.113.7", NOW) is True
    assert limiter.allow("203.0.113.7", NOW + timedelta(minutes=20)) is True
    assert limiter.allow("203.0.113.7", NOW + timedelta(minutes=40)) is False


def test_visitors_are_counted_separately(table: TableClient) -> None:
    limiter = RateLimitService(table, salt="salt", per_10_min=1, per_day=30)

    assert limiter.allow("203.0.113.7", NOW) is True
    assert limiter.allow("198.51.100.4", NOW) is True


def test_raw_ip_is_not_stored(table: TableClient) -> None:
    limiter = RateLimitService(table, salt="salt", per_10_min=1, per_day=30)

    limiter.allow("203.0.113.7", NOW)

    assert table.get_number("rate#203.0.113.7#day#2026-12-05", "count") == 0
