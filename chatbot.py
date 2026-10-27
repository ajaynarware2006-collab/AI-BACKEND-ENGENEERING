from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("nvidia_api_key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

while True:

    userinput = input("\nYou : ")
    if userinput.lower() == "exit":
        break
    completion = client.chat.completions.create(

        extra_body={},
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[
            {
                "role" : "user",
                "content" : f"{userinput}"
            }
        ],
        stream=True
    )
    print("Bot : ",end="")
    for words in completion:
        
        print(words.choices[0].delta.content,end="" , flush=True)