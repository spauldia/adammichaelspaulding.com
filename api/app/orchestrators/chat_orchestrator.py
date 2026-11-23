"""Answers one chat request."""

import logging
from datetime import UTC, datetime

import anthropic

from app.clients.anthropic_client import ClaudeClient, message_text
from app.constants import REFUSAL_REPLY, ModelPrices
from app.models import ChatRequest, ChatResponse
from app.services.budget_service import BudgetService, calculate_cost_micro_usd
from app.services.rate_limit_service import RateLimitService

logger = logging.getLogger(__name__)


class ChatOrchestrator:
    """Checks the limits, asks Claude and records the cost."""

    def __init__(
        self,
        claude: ClaudeClient,
        budget: BudgetService,
        rate_limit: RateLimitService,
        system_prompt: str,
        prices: ModelPrices,
    ) -> None:
        self._claude = claude
        self._budget = budget
        self._rate_limit = rate_limit
        self._system_prompt = system_prompt
        self._prices = prices

    def answer(self, request: ChatRequest, client_ip: str) -> ChatResponse:
        """Return the reply for the visitor's latest question."""
        now = datetime.now(UTC)
        if not self._rate_limit.allow(client_ip, now):
            return ChatResponse(kind="rate_limited")
        if self._budget.is_exhausted(now):
            return ChatResponse(kind="budget")

        try:
            message = self._claude.create_message(self._system_prompt, request.to_message_params())
        except anthropic.APIError:
            logger.exception("Claude request failed")
            return ChatResponse(kind="budget")

        self._budget.record_spend(now, calculate_cost_micro_usd(message.usage, self._prices))
        text = message_text(message)
        if message.stop_reason == "refusal" or not text:
            return ChatResponse(kind="answer", reply=REFUSAL_REPLY)
        return ChatResponse(kind="answer", reply=text)
