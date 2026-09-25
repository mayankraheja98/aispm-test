"""vLLM OpenAI-compatible server at localhost:8000."""
import os
from openai import OpenAI

# vLLM self-hosted server
VLLM_BASE_URL = "http://localhost:8000/v1"

client = OpenAI(
    base_url=VLLM_BASE_URL,
    api_key="EMPTY",  # vLLM does not need a real key
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "What colours are trending this season?"}],
    temperature=0.7,
)
print(response.choices[0].message.content)
