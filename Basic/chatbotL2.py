
import os
import json

from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

api_key = os.getenv("nvidia_api_key")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

# 2. Create API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    timeout=60.0,
    max_retries=2,
)

# 3. Chat history file
HISTORY_FILE = "chat_history.json"

# 4. Load previous chat history
def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            raise ValueError("Invalid chat history format.")

        # Validate stored messages
        for message in history:
            if (
                not isinstance(message, dict)
                or message.get("role") not in ("user", "assistant")
                or not isinstance(message.get("content"), str)
            ):
                raise ValueError("Invalid message in chat history.")

        return history

    except (json.JSONDecodeError, ValueError) as error:
        print(f"Could not load history: {error}")
        return []

# 5. Save chat history
def save_history(history):

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

# 6. Initialize conversation memory
chat_history = load_history()

print("\nAI Chatbot Started!")
print("Commands: /clear, /exit\n")

if chat_history:
    print("Previous conversation loaded!\n")

# 7. Main chatbot loop
while True:

    try:
        userinput = input("You: ").strip()

        # Exit command
        if userinput.lower() in ("/exit", "exit", "quit"):
            print("Bot: Goodbye!")
            break

        # Empty input
        if not userinput:
            print("Bot: Please enter a message.\n")
            continue

        # Clear conversation
        if userinput.lower() == "/clear":

            chat_history.clear()
            save_history(chat_history)

            print("Bot: Conversation memory cleared!\n")
            continue

        # Add user message to memory
        chat_history.append({
            "role": "user",
            "content": userinput
        })

        print("Bot: ", end="", flush=True)

        assistant_response = ""

        # 8. Send complete conversation to AI
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=chat_history,
            stream=True,
        )

        # 9. Receive streamed response
        for chunk in completion:

            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                print(content, end="", flush=True)
                assistant_response += content

        print("\n")

        # 10. Save assistant response
        if assistant_response:

            chat_history.append({
                "role": "assistant",
                "content": assistant_response
            })

            save_history(chat_history)

        else:
            # Remove unanswered user message
            chat_history.pop()
            print("Bot: No response received.\n")

    except KeyboardInterrupt:
        print("\nBot: Chatbot stopped.")
        break

    except Exception as error:

        # Remove user message if request failed
        if chat_history and chat_history[-1]["role"] == "user":
            chat_history.pop()

        print(f"\nBot: Something went wrong: {error}\n")