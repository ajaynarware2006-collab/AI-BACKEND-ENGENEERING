from types import SimpleNamespace

from utils.response_parser import AIResponseParser


def test_parse_valid_response():

    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    role="assistant",
                    content="Hello bro!"
                ),
                finish_reason="stop"
            )
        ],
        model="test-model",
        usage=SimpleNamespace(
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15
        )
    )

    result = AIResponseParser.parse(response)

    assert result["success"] is True
    assert result["content"] == "Hello bro!"
    assert result["role"] == "assistant"
    assert result["usage"]["total_tokens"] == 15


def test_parse_invalid_response():

    result = AIResponseParser.parse(None)

    assert result["success"] is False
    assert result["content"] is None


def test_parse_stream_chunk():

    chunk = SimpleNamespace(
        choices=[
            SimpleNamespace(
                delta=SimpleNamespace(
                    content="Hello"
                )
            )
        ]
    )

    result = AIResponseParser.parse_stream_chunk(chunk)

    assert result == "Hello"


def test_parse_empty_stream_chunk():

    chunk = SimpleNamespace(
        choices=[
            SimpleNamespace(
                delta=SimpleNamespace(
                    content=None
                )
            )
        ]
    )

    result = AIResponseParser.parse_stream_chunk(chunk)

    assert result == ""