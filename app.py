"""
SaaS AI API Consumer — Myntra Content Generation Service
Detection signals: anthropic.Anthropic(), openai.OpenAI(), cohere.Client()
Asset type: 3rd_party_model_saas
"""
import os
from typing import Optional

import anthropic
import openai
import cohere
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Myntra Content Generation API")

# ── Clients ────────────────────────────────────────────────────────────────────
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))


# ── Request/Response Models ────────────────────────────────────────────────────

class ProductDescriptionRequest(BaseModel):
    product_name: str
    category: str
    key_features: list[str]
    target_audience: str
    tone: str = "friendly"


class SEOTagRequest(BaseModel):
    product_name: str
    category: str
    description: str
    max_tags: int = 10


class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "hi"


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.post("/generate/product-description")
async def generate_product_description(req: ProductDescriptionRequest) -> dict:
    """Generate compelling product descriptions using Claude."""
    prompt = f"""Write a compelling product description for:
Product: {req.product_name}
Category: {req.category}
Key Features: {', '.join(req.key_features)}
Target Audience: {req.target_audience}
Tone: {req.tone}

Write 3-4 sentences. Be specific, engaging, and highlight benefits over features."""

    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"description": message.content[0].text}


@app.post("/generate/seo-tags")
async def generate_seo_tags(req: SEOTagRequest) -> dict:
    """Generate SEO-optimized tags using GPT-4o."""
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an SEO expert for e-commerce fashion."},
            {"role": "user", "content": f"Generate {req.max_tags} SEO tags for: {req.product_name} | Category: {req.category} | {req.description}. Return as JSON array of strings."},
        ],
        response_format={"type": "json_object"},
        max_tokens=200,
    )
    return {"tags": response.choices[0].message.content}


@app.post("/generate/embeddings")
async def generate_embeddings(texts: list[str]) -> dict:
    """Generate product embeddings for semantic search using Cohere."""
    response = cohere_client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document",
    )
    return {"embeddings": response.embeddings, "count": len(texts)}


@app.post("/generate/translate")
async def translate_product(req: TranslationRequest) -> dict:
    """Translate product text for regional markets."""
    message = anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Translate the following from {req.source_lang} to {req.target_lang}. Return only the translation:\n\n{req.text}"
        }],
    )
    return {"translation": message.content[0].text, "target_lang": req.target_lang}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
