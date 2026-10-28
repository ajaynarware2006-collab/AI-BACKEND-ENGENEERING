
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

api_key = os.getenv("nvidia_api_key")

# 2. Check API key
if not api_key:
    raise ValueError(
        "API key not found. Please check your .env file."
    )

# 3. Create API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    timeout=60.0,
    max_retries=2,
)

print("AI Chatbot started!")
print("Type 'exit' or 'quit' to stop.\n")

# 4. Main chatbot loop
while True:
    try:
        userinput = input("You: ").strip()

        # Exit command
        if userinput.lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break

        # Handle empty input
        if not userinput:
            print("Bot: Please enter a message.\n")
            continue

        print("Bot: ", end="", flush=True)

        # 5. Send request to AI
        completion = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {
                    "role": "user",
                    "content": userinput,
                }
            ],
            stream=True,
        )

        # 6. Print streamed response
        for chunk in completion:
            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                print(content, end="", flush=True)

        print("\n")

    except KeyboardInterrupt:
        print("\nBot: Chatbot stopped.")
        break

    except Exception as error:
        print(f"\nBot: Something went wrong: {error}\n")