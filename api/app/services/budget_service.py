"""Tracks how much the chat model has cost this month."""

import math
from datetime import datetime

from anthropic.types import Usage

from app.clients.dynamodb_client import TableClient
from app.constants import BUDGET_ITEM_TTL_SECONDS, ModelPrices

SPENT_ATTRIBUTE = "spent_micro_usd"


class BudgetService:
    """Reads and records monthly spend in micro-dollars."""

    def __init__(self, table: TableClient, monthly_budget_micro_usd: int) -> None:
        self._table = table
        self._limit = monthly_budget_micro_usd

    def is_exhausted(self, now: datetime) -> bool:
        """Return True when this month's spend has reached the budget."""
        return self._table.get_number(budget_key(now), SPENT_ATTRIBUTE) >= self._limit

    def record_spend(self, now: datetime, amount_micro_usd: int) -> None:
        """Add one response's cost to this month's total."""
        expires_at = int(now.timestamp()) + BUDGET_ITEM_TTL_SECONDS
        self._table.add_number(budget_key(now), SPENT_ATTRIBUTE, amount_micro_usd, expires_at)


def budget_key(now: datetime) -> str:
    """Return the table key for the month of the given time."""
    return f"budget#{now:%Y-%m}"


def calculate_cost_micro_usd(usage: Usage, prices: ModelPrices) -> int:
    """Return the cost of one response in micro-dollars, rounded up."""
    cost = (
        usage.input_tokens * prices.input
        + (usage.cache_creation_input_tokens or 0) * prices.cache_write
        + (usage.cache_read_input_tokens or 0) * prices.cache_read
        + usage.output_tokens * prices.output
    )
    return math.ceil(cost)
