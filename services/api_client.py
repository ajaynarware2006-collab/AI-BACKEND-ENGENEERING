"""
Centralized AI API Client Manager.

Provides reusable API communication,
connection management, error handling
and streaming support.
"""

from typing import Iterator, Optional

from openai import OpenAI, APIError, APITimeoutError
from openai import AuthenticationError, RateLimitError

from config.settings import get_settings
from config.logger import get_logger


logger = get_logger("api_client")


class AIAPIClient:
    """Manages communication with AI providers."""

    def __init__(self):

        self.settings = get_settings()

        self.client: Optional[OpenAI] = None

        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the API client."""

        api_key = self.settings.require_openrouter_api_key()

        self.client = OpenAI(
            base_url=self.settings.openrouter_base_url,
            api_key=api_key,
            timeout=self.settings.request_timeout,
            max_retries=self.settings.max_retries,
        )

        logger.info("AI API client initialized successfully.")

    def get_client(self) -> OpenAI:
        """Return the initialized API client."""

        if self.client is None:
            raise RuntimeError("API client is not initialized.")

        return self.client

    def generate_response(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        stream: bool = False,
    ):
        """
        Generate an AI response.

        Args:
            messages: Conversation messages.
            model: AI model identifier.
            stream: Enable streaming response.

        Returns:
            API response or streaming iterator.
        """

        selected_model = model or self.settings.default_model

        logger.info(
            "Sending request to AI model: %s",
            selected_model
        )

        try:

            response = self.get_client().chat.completions.create(
                model=selected_model,
                messages=messages,
                stream=stream,
            )

            logger.info("AI API request completed successfully.")

            return response

        except AuthenticationError:
            logger.error("AI API authentication failed.")
            raise

        except RateLimitError:
            logger.warning("AI API rate limit exceeded.")
            raise

        except APITimeoutError:
            logger.error("AI API request timed out.")
            raise

        except APIError:
            logger.exception("AI API returned an error.")
            raise

        except Exception:
            logger.exception("Unexpected error during AI request.")
            raise

    def close(self) -> None:
        """Close the API client connection."""

        if self.client is not None:
            self.client.close()
            self.client = None

            logger.info("AI API client closed.")


# Shared client instance
ai_client = AIAPIClient()