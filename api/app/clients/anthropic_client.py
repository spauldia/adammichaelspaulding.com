"""Thin wrapper around the Claude Messages API."""

import anthropic
from anthropic.types import Message, MessageParam, TextBlockParam

from app.constants import CLAUDE_MAX_RETRIES, CLAUDE_TIMEOUT_SECONDS, MAX_OUTPUT_TOKENS


class ClaudeClient:
    """Sends chat requests to Claude."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client = anthropic.Anthropic(
            api_key=api_key, timeout=CLAUDE_TIMEOUT_SECONDS, max_retries=CLAUDE_MAX_RETRIES
        )
        self._model = model

    def create_message(self, system_prompt: str, messages: list[MessageParam]) -> Message:
        """Return Claude's response to the conversation."""
        return self._client.messages.create(
            model=self._model,
            max_tokens=MAX_OUTPUT_TOKENS,
            system=[TextBlockParam(type="text", text=system_prompt, cache_control={"type": "ephemeral"})],
            output_config={"effort": "low"},
            messages=messages,
        )


def message_text(message: Message) -> str:
    """Return the text blocks of a response joined together."""
    return "".join(block.text for block in message.content if block.type == "text").strip()
