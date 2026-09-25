"""DeepSeek API client (api.deepseek.com)."""
import os
from openai import OpenAI

DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1"
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_ENDPOINT,
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "What are K-fashion trends in 2025?"}],
)
print(response.choices[0].message.content)
