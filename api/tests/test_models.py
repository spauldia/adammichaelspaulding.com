import pytest
from pydantic import ValidationError

from app.models import ChatRequest


def test_accepts_a_single_question() -> None:
    request = ChatRequest.model_validate({"messages": [{"role": "user", "content": "Hi"}]})

    assert request.to_message_params() == [{"role": "user", "content": "Hi"}]


def test_accepts_alternating_turns() -> None:
    request = ChatRequest.model_validate(
        {
            "messages": [
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "Hello"},
                {"role": "user", "content": "What does Adam do?"},
            ]
        }
    )

    assert len(request.messages) == 3


@pytest.mark.parametrize(
    "messages",
    [
        [],
        [{"role": "assistant", "content": "Hello"}],
        [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}],
        [{"role": "user", "content": "Hi"}, {"role": "user", "content": "Hi again"}],
        [{"role": "user", "content": "x" * 501}],
        [{"role": "user", "content": ""}],
        [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}] * 4
        + [{"role": "user", "content": "Hi"}],
    ],
)
def test_rejects_invalid_conversations(messages: list[dict[str, str]]) -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate({"messages": messages})
