"""
Request validation module for AI Backend Engineering Lab.

Validates user messages, conversation history,
and AI model configuration.
"""

import re
from typing import Literal

from pydantic import BaseModel
from pydantic import Field, field_validator
from pydantic import ConfigDict


# Validation configuration
MAX_MESSAGE_LENGTH = 10000
MAX_CONVERSATION_MESSAGES = 50

ALLOWED_ROLES = {"user", "assistant"}

MODEL_PATTERN = re.compile(
    r"^[a-zA-Z0-9][a-zA-Z0-9._:/-]{0,199}$"
)


class ChatMessage(BaseModel):
    """Validate individual chat messages."""

    model_config = ConfigDict(extra="forbid")

    role: Literal["user", "assistant"]

    content: str = Field(
        min_length=1,
        max_length=MAX_MESSAGE_LENGTH
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        return value


class ChatRequest(BaseModel):
    """Validate incoming chat requests."""

    model_config = ConfigDict(extra="forbid")

    messages: list[ChatMessage] = Field(
        min_length=1,
        max_length=MAX_CONVERSATION_MESSAGES
    )

    model: str = Field(
        default="nvidia/nemotron-3-ultra-550b-a55b:free",
        min_length=1,
        max_length=200
    )

    stream: bool = False

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:

        value = value.strip()

        if not MODEL_PATTERN.fullmatch(value):
            raise ValueError("Invalid model identifier.")

        return value


def validate_chat_request(data: dict) -> ChatRequest:
    """
    Validate incoming chat request data.

    Args:
        data: Raw request dictionary.

    Returns:
        Validated ChatRequest object.
    """

    return ChatRequest.model_validate(data)


def validate_message(message: str) -> str:
    """
    Validate a single user message.
    """

    if not isinstance(message, str):
        raise ValueError("Message must be a string.")

    message = message.strip()

    if not message:
        raise ValueError("Message cannot be empty.")

    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError("Message exceeds maximum length.")

    return message