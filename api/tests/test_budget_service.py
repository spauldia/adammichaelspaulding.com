from datetime import UTC, datetime

from anthropic.types import Usage

from app.clients.dynamodb_client import TableClient
from app.constants import MODEL_PRICES
from app.services.budget_service import BudgetService, budget_key, calculate_cost_micro_usd

NOW = datetime(2026, 12, 5, 15, 30, tzinfo=UTC)


def test_is_not_exhausted_before_any_spend(table: TableClient) -> None:
    budget = BudgetService(table, monthly_budget_micro_usd=4_500_000)

    assert budget.is_exhausted(NOW) is False


def test_is_exhausted_once_spend_reaches_the_limit(table: TableClient) -> None:
    budget = BudgetService(table, monthly_budget_micro_usd=1_000)

    budget.record_spend(NOW, 600)
    assert budget.is_exhausted(NOW) is False

    budget.record_spend(NOW, 400)
    assert budget.is_exhausted(NOW) is True


def test_spend_resets_in_a_new_month(table: TableClient) -> None:
    budget = BudgetService(table, monthly_budget_micro_usd=1_000)
    budget.record_spend(NOW, 1_000)

    assert budget.is_exhausted(datetime(2027, 1, 1, tzinfo=UTC)) is False


def test_budget_key_uses_the_month() -> None:
    assert budget_key(NOW) == "budget#2026-12"


def test_calculate_cost_counts_every_token_type() -> None:
    usage = Usage.model_construct(
        input_tokens=1_000,
        output_tokens=500,
        cache_creation_input_tokens=4_000,
        cache_read_input_tokens=8_000,
    )

    cost = calculate_cost_micro_usd(usage, MODEL_PRICES["claude-haiku-5-5"])

    # 1000 * 0.10 + 4000 * 0.125 + 8000 * 0.01 + 500 * 0.50 = 930 micro-dollars
    assert cost == 930


def test_calculate_cost_treats_missing_cache_counts_as_zero() -> None:
    usage = Usage.model_construct(
        input_tokens=10, output_tokens=1, cache_creation_input_tokens=None, cache_read_input_tokens=None
    )

    assert calculate_cost_micro_usd(usage, MODEL_PRICES["claude-haiku-5-5"]) == 2
