"""
Self-hosted LLM Inference — Myntra Internal Moderation Service
Detection signals: llama-cpp-python, ollama, self-hosted model
Asset type: 3rd_party_model_hosted
"""
import os
import ollama
from llama_cpp import Llama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Myntra Content Moderation LLM")

# Ollama-based inference (Llama 3 running locally on GPU VMs)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# llama.cpp for low-latency keyword moderation on CPU
GGUF_MODEL_PATH = os.getenv("GGUF_PATH", "/models/llama-3.1-8b-instruct.Q4_K_M.gguf")
llama_model = None  # Lazy load


class ModerationRequest(BaseModel):
    content: str
    context: str = "product_review"


class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 200


@app.post("/moderate")
async def moderate_content(req: ModerationRequest) -> dict:
    """Check if user-generated content violates Myntra's policies (runs on-prem, no data leaves Myntra)."""
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": "You are a content moderation classifier. Return JSON: {safe: bool, reason: str}"},
            {"role": "user", "content": f"Context: {req.context}\nContent: {req.content}"},
        ],
    )
    return {"result": response["message"]["content"]}


@app.post("/generate/fast")
async def generate_fast(req: GenerationRequest) -> dict:
    """Low-latency generation using llama.cpp (CPU inference for short outputs)."""
    global llama_model
    if llama_model is None:
        llama_model = Llama(model_path=GGUF_MODEL_PATH, n_ctx=2048, n_threads=8)

    output = llama_model(req.prompt, max_tokens=req.max_tokens, echo=False)
    return {"text": output["choices"][0]["text"]}


@app.get("/health")
async def health():
    return {"status": "ok", "model": OLLAMA_MODEL}
