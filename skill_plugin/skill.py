"""
Claude Skill — Myntra Style Assistant
Detection signals: SKILL.md present + openai/anthropic imports
Asset type: skill_plugin
"""
import os
import anthropic
from pydantic import BaseModel

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class StyleQuery(BaseModel):
    occasion: str
    budget_max: int
    gender: str = "any"
    preferences: list[str] = []


def search_products(query: str, category: str = "", limit: int = 5) -> list[dict]:
    """Tool: Search Myntra catalog."""
    # Production: calls catalog API
    return [{"id": "P001", "name": "Blue Kurta", "price": 899}]


def get_outfit_suggestions(query: StyleQuery) -> str:
    """Main skill entrypoint: generate outfit recommendations."""
    tools = [
        {
            "name": "search_products",
            "description": "Search Myntra's product catalog",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["query"],
            },
        }
    ]

    messages = [{
        "role": "user",
        "content": f"Create an outfit for: {query.occasion} | Budget: ₹{query.budget_max} | Gender: {query.gender} | Preferences: {', '.join(query.preferences)}"
    }]

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        tools=tools,
        messages=messages,
    )
    return response.content[0].text if response.content else "Could not generate suggestions."
