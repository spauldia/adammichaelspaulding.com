import json
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_chat_orchestrator
from app.main import app, handler
from app.models import ChatResponse


@pytest.fixture
def orchestrator() -> Iterator[MagicMock]:
    fake = MagicMock()
    fake.answer.return_value = ChatResponse(kind="answer", reply="Adam builds data platforms.")
    app.dependency_overrides[get_chat_orchestrator] = lambda: fake
    yield fake
    app.dependency_overrides.clear()


def function_url_event(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a Lambda Function URL event (payload format 2.0)."""
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": path,
        "rawQueryString": "",
        "headers": {"content-type": "application/json", "host": "example.lambda-url.us-east-1.on.aws"},
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "example",
            "domainName": "example.lambda-url.us-east-1.on.aws",
            "domainPrefix": "example",
            "http": {
                "method": method,
                "path": path,
                "protocol": "HTTP/1.1",
                "sourceIp": "203.0.113.7",
                "userAgent": "pytest",
            },
            "requestId": "request-id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "05/Dec/2026:15:30:00 +0000",
            "timeEpoch": 1796484600000,
        },
        "body": json.dumps(body) if body else None,
        "isBase64Encoded": False,
    }


def test_health() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_the_orchestrator_reply(orchestrator: MagicMock) -> None:
    response = TestClient(app).post("/chat", json={"messages": [{"role": "user", "content": "Hi"}]})

    assert response.status_code == 200
    assert response.json() == {"kind": "answer", "reply": "Adam builds data platforms."}


def test_chat_rejects_an_invalid_conversation(orchestrator: MagicMock) -> None:
    response = TestClient(app).post("/chat", json={"messages": [{"role": "assistant", "content": "Hi"}]})

    assert response.status_code == 422
    orchestrator.answer.assert_not_called()


def test_lambda_handler_passes_the_visitor_ip(orchestrator: MagicMock) -> None:
    event = function_url_event("POST", "/chat", {"messages": [{"role": "user", "content": "Hi"}]})

    result = handler(event, MagicMock())

    assert result["statusCode"] == 200
    assert json.loads(result["body"])["reply"] == "Adam builds data platforms."
    assert orchestrator.answer.call_args.args[1] == "203.0.113.7"
