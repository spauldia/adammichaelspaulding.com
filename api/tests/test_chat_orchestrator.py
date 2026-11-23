from datetime import UTC, datetime
from unittest.mock import MagicMock

import anthropic
import httpx2
import pytest
from anthropic.types import Message

from app.clients.dynamodb_client import TableClient
from app.constants import MODEL_PRICES, REFUSAL_REPLY
from app.models import ChatRequest
from app.orchestrators.chat_orchestrator import ChatOrchestrator
from app.services.budget_service import SPENT_ATTRIBUTE, BudgetService, budget_key
from app.services.rate_limit_service import RateLimitService
from tests.conftest import make_message

REQUEST = ChatRequest.model_validate({"messages": [{"role": "user", "content": "What does Adam do?"}]})
CLIENT_IP = "203.0.113.7"


def build_orchestrator(
    table: TableClient, claude: MagicMock, budget_micro_usd: int = 4_500_000, per_10_min: int = 10
) -> ChatOrchestrator:
    return ChatOrchestrator(
        claude=claude,
        budget=BudgetService(table, budget_micro_usd),
        rate_limit=RateLimitService(table, salt="salt", per_10_min=per_10_min, per_day=30),
        system_prompt="system prompt",
        prices=MODEL_PRICES["claude-haiku-5-5"],
    )


def fake_claude(result: Message | Exception) -> MagicMock:
    claude = MagicMock()
    if isinstance(result, Exception):
        claude.create_message.side_effect = result
    else:
        claude.create_message.return_value = result
    return claude


def this_month_spend(table: TableClient) -> int:
    return table.get_number(budget_key(datetime.now(UTC)), SPENT_ATTRIBUTE)


def test_returns_the_answer_and_records_its_cost(table: TableClient) -> None:
    claude = fake_claude(make_message("Adam is a backend engineer."))

    response = build_orchestrator(table, claude).answer(REQUEST, CLIENT_IP)

    assert response.kind == "answer"
    assert response.reply == "Adam is a backend engineer."
    claude.create_message.assert_called_once_with("system prompt", [{"role": "user", "content": "What does Adam do?"}])
    # 1000 input tokens * 0.10 + 200 output tokens * 0.50
    assert this_month_spend(table) == 200


def test_rate_limited_visitor_does_not_reach_claude(table: TableClient) -> None:
    claude = fake_claude(make_message("unused"))
    orchestrator = build_orchestrator(table, claude, per_10_min=1)
    orchestrator.answer(REQUEST, CLIENT_IP)
    claude.create_message.reset_mock()

    response = orchestrator.answer(REQUEST, CLIENT_IP)

    assert response.kind == "rate_limited"
    claude.create_message.assert_not_called()


def test_spent_budget_does_not_reach_claude(table: TableClient) -> None:
    claude = fake_claude(make_message("unused"))

    response = build_orchestrator(table, claude, budget_micro_usd=0).answer(REQUEST, CLIENT_IP)

    assert response.kind == "budget"
    claude.create_message.assert_not_called()


@pytest.mark.parametrize(
    "error",
    [
        anthropic.APIConnectionError(request=httpx2.Request("POST", "https://api.anthropic.com/v1/messages")),
        anthropic.APITimeoutError(request=httpx2.Request("POST", "https://api.anthropic.com/v1/messages")),
    ],
)
def test_claude_error_returns_the_budget_reply(table: TableClient, error: Exception) -> None:
    response = build_orchestrator(table, fake_claude(error)).answer(REQUEST, CLIENT_IP)

    assert response.kind == "budget"
    assert this_month_spend(table) == 0


def test_refusal_returns_the_refusal_reply(table: TableClient) -> None:
    claude = fake_claude(make_message("", stop_reason="refusal"))

    response = build_orchestrator(table, claude).answer(REQUEST, CLIENT_IP)

    assert response.kind == "answer"
    assert response.reply == REFUSAL_REPLY


def test_unexpected_error_propagates(table: TableClient) -> None:
    claude = fake_claude(RuntimeError("bug"))

    with pytest.raises(RuntimeError):
        build_orchestrator(table, claude).answer(REQUEST, CLIENT_IP)
