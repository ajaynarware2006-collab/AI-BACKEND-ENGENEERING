from typing import Any


class AIResponseParser:
    """
    Converts raw AI API responses into a
    standardized application-friendly format.
    """

    @staticmethod
    def parse(response: Any) -> dict:
        """
        Extracts useful information from an
        OpenAI-compatible Chat Completion response.
        """

        try:
            choice = response.choices[0]

            message = choice.message

            return {
                "success": True,
                "content": message.content or "",
                "role": message.role,
                "model": response.model,
                "finish_reason": choice.finish_reason,
                "usage": AIResponseParser._parse_usage(
                    response.usage
                ),
                "error": None
            }

        except (AttributeError, IndexError, TypeError) as error:

            return {
                "success": False,
                "content": None,
                "role": None,
                "model": None,
                "finish_reason": None,
                "usage": None,
                "error": f"Invalid AI response: {error}"
            }

    @staticmethod
    def _parse_usage(usage: Any) -> dict | None:
        """
        Extracts token usage information.
        """

        if usage is None:
            return None

        return {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }

    @staticmethod
    def parse_stream_chunk(chunk: Any) -> str:
        """
        Extracts generated text from a streaming chunk.
        """

        try:
            content = chunk.choices[0].delta.content

            return content or ""

        except (AttributeError, IndexError, TypeError):
            return ""
