import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "user",
                "content": "Explain Python functions in simple words with one example."
            }
        ],
        "stream": False
    }
)

data = response.json()

print(data["message"]["content"])
print()
print(response)