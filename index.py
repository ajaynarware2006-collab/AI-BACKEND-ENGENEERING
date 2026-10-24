from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("Gemini_api_key")

if not API_KEY:
    raise ValueError("API Key not found")

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Eplain Python function in simple words with one example."
)

print(response.text)
print()
print(response)