# Myntra Style Assistant Skill

A Claude skill that helps users with fashion recommendations, outfit coordination, and style queries using Myntra's product catalog.

## Capabilities

- Search and recommend outfits based on occasion, body type, and preferences
- Coordinate looks from Myntra's catalog
- Provide styling tips and trend analysis

## Usage

This skill is invoked when a user asks Claude for fashion advice or outfit recommendations.

```python
# Skill entrypoint
from skill import StyleAssistantSkill

skill = StyleAssistantSkill()
result = skill.run(query="suggest a formal outfit for a business meeting")
```

## Configuration

Set `MYNTRA_API_KEY` in your environment to enable live catalog search.
