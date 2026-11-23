"""Request and response models for the chat API."""

from typing import Literal

from anthropic.types import AssistantMessageParam, MessageParam, UserMessageParam
from pydantic import BaseModel, Field, model_validator

from app.constants import MAX_QUESTION_CHARS, MAX_TURN_CHARS, MAX_TURNS


class ChatTurn(BaseModel):
    """One message in the conversation."""

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_TURN_CHARS)

    def to_message_param(self) -> MessageParam:
        """Return the turn in the Claude API message format."""
        if self.role == "user":
            return UserMessageParam(role="user", content=self.content)
        return AssistantMessageParam(role="assistant", content=self.content)


class ChatRequest(BaseModel):
    """The recent conversation, ending with the visitor's new question."""

    messages: list[ChatTurn] = Field(min_length=1, max_length=MAX_TURNS)

    @model_validator(mode="after")
    def check_turn_order(self) -> "ChatRequest":
        if self.messages[0].role != "user" or self.messages[-1].role != "user":
            raise ValueError("Conversation must start and end with a user message")
        for previous, current in zip(self.messages, self.messages[1:], strict=False):
            if previous.role == current.role:
                raise ValueError("Messages must alternate between user and assistant")
        if len(self.messages[-1].content) > MAX_QUESTION_CHARS:
            raise ValueError(f"Question must be {MAX_QUESTION_CHARS} characters or fewer")
        return self

    def to_message_params(self) -> list[MessageParam]:
        """Return the conversation in the Claude API message format."""
        return [turn.to_message_param() for turn in self.messages]


class ChatResponse(BaseModel):
    """The reply shown in the chat widget."""

    kind: Literal["answer", "rate_limited", "budget"]
    reply: str = ""


class HealthResponse(BaseModel):
    """The health check result."""

    status: Literal["ok"] = "ok"
