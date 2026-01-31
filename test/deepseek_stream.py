from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instantiate DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def stream_chat(prompt: str):
    response = client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in response:
        print(chunk.choices[0].delta.content, end="", flush=True)

if __name__ == "__main__":
    stream_chat("Can you do streaming output?")