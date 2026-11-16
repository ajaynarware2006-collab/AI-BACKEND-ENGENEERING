import pytest

from memory.conversation_memory import ConversationMemory


def test_add_message():

    memory = ConversationMemory()

    memory.add_message("user", "Hello")

    assert memory.get_message_count() == 1


def test_add_multiple_messages():

    memory = ConversationMemory()

    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi!")

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_message_limit():

    memory = ConversationMemory(max_messages=2)

    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Message 2")
    memory.add_message("user", "Message 3")

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["content"] == "Message 2"


def test_invalid_role():

    memory = ConversationMemory()

    with pytest.raises(ValueError):
        memory.add_message("system", "Hello")


def test_empty_message():

    memory = ConversationMemory()

    with pytest.raises(ValueError):
        memory.add_message("user", "   ")


def test_clear_memory():

    memory = ConversationMemory()

    memory.add_message("user", "Hello")
    memory.clear()

    assert memory.get_message_count() == 0


def test_last_message():

    memory = ConversationMemory()

    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi!")

    last_message = memory.get_last_message()

    assert last_message["content"] == "Hi!"


def test_empty_last_message():

    memory = ConversationMemory()

    assert memory.get_last_message() is None