"""Shared test fixtures."""

from collections.abc import Iterator

import boto3
import pytest
from anthropic.types import Message, TextBlock, Usage
from moto import mock_aws

from app.clients.dynamodb_client import TableClient

TABLE_NAME = "site-chat-test"


@pytest.fixture(autouse=True)
def aws_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.delenv("AWS_PROFILE", raising=False)


@pytest.fixture
def table() -> Iterator[TableClient]:
    with mock_aws():
        boto3.client("dynamodb").create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield TableClient(TABLE_NAME)


def make_message(text: str, stop_reason: str = "end_turn") -> Message:
    """Build a Claude response for tests."""
    return Message.model_construct(
        id="msg_test",
        type="message",
        role="assistant",
        model="claude-haiku-5-5",
        content=[TextBlock.model_construct(type="text", text=text)],
        stop_reason=stop_reason,
        usage=Usage.model_construct(
            input_tokens=1000,
            output_tokens=200,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
        ),
    )
