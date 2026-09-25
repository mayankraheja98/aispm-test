"""Myntra fashion chatbot with injected system prompt."""
import os
import yaml
from openai import OpenAI

with open("config.yaml") as f:
    config = yaml.safe_load(f)

with open(config["chatbot"]["system_prompt_file"]) as f:
    SYSTEM_PROMPT = f.read()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def chat(user_message: str) -> str:
    response = client.chat.completions.create(
        model=config["chatbot"]["model"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
