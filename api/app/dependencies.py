"""Builds the shared objects the routes use."""

from functools import cache

from app.clients.anthropic_client import ClaudeClient
from app.clients.dynamodb_client import TableClient
from app.clients.profile_client import fetch_profile_json
from app.clients.s3_client import ObjectClient
from app.clients.ssm_client import ParameterClient
from app.config import get_settings
from app.constants import MICRO_USD_PER_USD, MODEL_PRICES
from app.orchestrators.chat_orchestrator import ChatOrchestrator
from app.services.budget_service import BudgetService
from app.services.prompt_service import build_system_prompt
from app.services.rate_limit_service import RateLimitService


@cache
def get_chat_orchestrator() -> ChatOrchestrator:
    """Return the chat orchestrator, built once per Lambda container."""
    settings = get_settings()
    parameters = ParameterClient()
    table = TableClient(settings.table_name)
    notes = ObjectClient().get_text(settings.notes_bucket, settings.notes_key)
    return ChatOrchestrator(
        claude=ClaudeClient(parameters.get_secret(settings.anthropic_key_param), settings.model),
        budget=BudgetService(table, int(settings.monthly_budget_usd * MICRO_USD_PER_USD)),
        rate_limit=RateLimitService(
            table,
            parameters.get_secret(settings.ip_salt_param),
            settings.rate_limit_per_10_min,
            settings.rate_limit_per_day,
        ),
        system_prompt=build_system_prompt(fetch_profile_json(settings.profile_url), notes),
        prices=MODEL_PRICES[settings.model],
    )
