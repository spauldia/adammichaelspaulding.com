"""Shared constants for the chat API."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPrices:
    """USD prices per million tokens for one model."""

    input: float
    output: float
    cache_write: float
    cache_read: float


DEFAULT_MODEL = "claude-haiku-5-5"
MODEL_PRICES: dict[str, ModelPrices] = {
    DEFAULT_MODEL: ModelPrices(input=0.10, output=0.50, cache_write=0.125, cache_read=0.01),
}
MAX_OUTPUT_TOKENS = 2048
CLAUDE_TIMEOUT_SECONDS = 12.0
CLAUDE_MAX_RETRIES = 1

MICRO_USD_PER_USD = 1_000_000

MAX_TURNS = 7
MAX_TURN_CHARS = 8000
MAX_QUESTION_CHARS = 500

TEN_MINUTES_SECONDS = 600
ONE_DAY_SECONDS = 86_400
BUDGET_ITEM_TTL_SECONDS = 90 * ONE_DAY_SECONDS

PROFILE_TIMEOUT_SECONDS = 5

REFUSAL_REPLY = "I can only answer questions about Adam and his work, experience or hobbies."
