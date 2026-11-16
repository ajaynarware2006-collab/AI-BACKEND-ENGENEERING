import pytest

from pydantic import ValidationError

from validators.validators import (
    ChatMessage,
    ChatRequest,
    validate_message,
    validate_chat_request,
)


def test_valid_message():

    message = validate_message("Hello AI")

    assert message == "Hello AI"


def test_empty_message():

    with pytest.raises(ValueError):
        validate_message("   ")


def test_valid_chat_message():

    message = ChatMessage(
        role="user",
        content="Hello AI"
    )

    assert message.role == "user"


def test_invalid_role():

    with pytest.raises(ValidationError):

        ChatMessage(
            role="admin",
            content="Hello"
        )


def test_valid_chat_request():

    request = validate_chat_request({
        "messages": [
            {
                "role": "user",
                "content": "Hello"
            }
        ],
        "stream": True
    })

    assert request.stream is True


def test_invalid_chat_request():

    with pytest.raises(ValidationError):

        ChatRequest(
            messages=[]
        )


def test_invalid_model():

    with pytest.raises(ValidationError):

        ChatRequest(
            messages=[
                {
                    "role": "user",
                    "content": "Hello"
                }
            ],
            model="invalid model name!"
        )