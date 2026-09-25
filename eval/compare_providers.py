"""Compare multiple LLM providers for fashion QA task."""
import os
import openai
import anthropic

PROMPT = "List 3 trending Indian fashion styles for 2025."

# OpenAI
oai = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
openai_resp = oai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": PROMPT}],
)

# Anthropic
ac = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
anthropic_resp = ac.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[{"role": "user", "content": PROMPT}],
)

# DeepSeek (api.deepseek.com)
ds = openai.OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)
deepseek_resp = ds.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": PROMPT}],
)

print("=== OpenAI ===", openai_resp.choices[0].message.content)
print("=== Anthropic ===", anthropic_resp.content[0].text)
print("=== DeepSeek ===", deepseek_resp.choices[0].message.content)
