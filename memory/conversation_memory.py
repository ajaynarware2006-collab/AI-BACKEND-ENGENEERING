from collections import deque
from threading import Lock


class ConversationMemory:
    """
    Manages conversation history for an AI chatbot.

    Features:
    - Stores user and assistant messages.
    - Maintains message order.
    - Limits conversation history.
    - Provides history in API-compatible format.
    - Supports clearing conversation history.
    """

    def __init__(self, max_messages: int = 20):

        if max_messages < 1:
            raise ValueError("max_messages must be at least 1")

        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)
        self.lock = Lock()

    def add_message(self, role: str, content: str) -> None:

        if role not in ("user", "assistant"):
            raise ValueError("Invalid message role")

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Message content cannot be empty")

        message = {
            "role": role,
            "content": content.strip()
        }

        with self.lock:
            self.messages.append(message)

    def get_history(self) -> list[dict]:

        with self.lock:
            return list(self.messages)

    def clear(self) -> None:

        with self.lock:
            self.messages.clear()

    def get_message_count(self) -> int:

        with self.lock:
            return len(self.messages)

    def get_last_message(self) -> dict | None:

        with self.lock:
            if not self.messages:
                return None

            return self.messages[-1].copy()