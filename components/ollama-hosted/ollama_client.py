"""Self-hosted Ollama at localhost:11434 — NOT a SaaS API call."""
import os
from openai import OpenAI

# Self-hosted Ollama: base_url points to localhost, not a cloud endpoint
OLLAMA_BASE = "http://localhost:11434/v1"

client = OpenAI(
    base_url=OLLAMA_BASE,
    api_key="ollama",  # dummy key for local Ollama
)

response = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "Describe Indo-western fusion style"}],
)
print(response.choices[0].message.content)
