"""Direct OpenAI & Anthropic SaaS API consumers."""
import os
import openai
import anthropic

# OpenAI
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Recommend a saree for Diwali"}],
)
print(response.choices[0].message.content)

# Anthropic
ac = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
msg = ac.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Suggest ethnic wear for wedding"}],
)
print(msg.content)
