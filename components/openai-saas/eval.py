"""Eval script for OpenAI integration."""
import os
import openai

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

test_cases = [
    "Find a red saree under ₹2000",
    "Recommend shoes for a formal office look",
]

for query in test_cases:
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
    )
    print(f"Q: {query}\nA: {r.choices[0].message.content}\n")
