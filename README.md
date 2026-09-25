# myntra-ai-spm-test

End-to-end test repository for the **Myntra AI-SPM** (AI Security Posture Management) scanner.

Each subdirectory under `components/` is designed to trigger a specific asset type classification and/or security flag when scanned.

## Component → Expected Classification

| Component | Expected Asset Type | Notes |
|---|---|---|
| `mcp-server` | `mcp_server` | FastMCP + `@mcp.tool` |
| `mcp-client` | `mcp_client` | `ClientSession` + `StdioServerParameters` |
| `langchain-agent` | `ai_agent_1st_party` | `AgentExecutor` + `Tool()` |
| `autogen-agent` | `ai_agent_1st_party` | AutoGen `AssistantAgent` |
| `crewai-agent` | `ai_agent_1st_party` | CrewAI `Crew` + `Agent` |
| `sklearn-model` | `1st_party_model` | `GridSearchCV` + `joblib.dump` + DVC |
| `pytorch-finetune` | `1st_party_model` | LoRA PEFT + `wandb.init` |
| `hf-finetune` | `1st_party_model` | `push_to_hub` |
| `dvc-model` | `1st_party_model` | `dvc.yaml` pipeline |
| `chromadb-rag` | `rag_pipeline` | ChromaDB + `RetrievalQA` |
| `faiss-rag` | `rag_pipeline` | `FAISS.from_documents` + `similarity_search` |
| `llamaindex-rag` | `rag_pipeline` | LlamaIndex `VectorStoreIndex` |
| `haystack-rag` | `rag_pipeline` | Haystack `Pipeline` + embedding retriever |
| `ragas-eval` | `rag_pipeline` | RAGAS (STRONG_RAG_LIB) |
| `prefect-pipeline` | `ai_pipeline` | `@flow` + `@task` |
| `openai-saas` | `3rd_party_model_saas` | OpenAI + Anthropic direct API |
| `azure-openai-saas` | `3rd_party_model_saas` | `*.openai.azure.com` endpoint |
| `azure-ai-foundry-saas` | `3rd_party_model_saas` | `*.services.ai.azure.com` |
| `bedrock-saas` | `3rd_party_model_saas` | `bedrock-runtime.*.amazonaws.com` |
| `vertex-saas` | `3rd_party_model_saas` | `*-aiplatform.googleapis.com` |
| `databricks-saas` | `3rd_party_model_saas` | `*.cloud.databricks.com` |
| `hf-inference-ep-saas` | `3rd_party_model_saas` | `*.aws.endpoints.huggingface.cloud` |
| `nvidia-nim-saas` | `3rd_party_model_saas` | `integrate.api.nvidia.com` |
| `watsonx-saas` | `3rd_party_model_saas` | `us-south.ml.cloud.ibm.com` |
| `deepseek-saas` | `3rd_party_model_saas` | `api.deepseek.com` |
| `ollama-hosted` | `3rd_party_model_hosted` | `localhost:11434` self-hosted |
| `vllm-hosted` | `3rd_party_model_hosted` | `localhost:8000` vLLM |
| `system-prompt-chatbot` | `system_prompt` | `system_prompt.txt` + config |
| `unsafe-serialization` | `1st_party_model` + 🚨 flags | `pickle.load`, `torch.load`, `joblib.load` |
| `safe-serialization` | `1st_party_model` + ✅ flags | `safetensors`, `weights_only=True` |

## GitHub Actions → Expected Classification

| Workflow | Expected Signal | Expected Type |
|---|---|---|
| `train-gpu.yml` | GPU runner + `dvc repro` + `WANDB_API_KEY` | `1st_party_model` |
| `hf-publish.yml` | `HF_TOKEN` + `push_to_hub` | `1st_party_model` |
| `serve-gpu.yml` | GPU runner only (no training) | `3rd_party_model_hosted` |
| `openai-eval.yml` | `OPENAI_API_KEY` injected | `3rd_party_model_saas` |
| `multi-provider.yml` | `ANTHROPIC_API_KEY` + `DEEPSEEK_API_KEY` | `3rd_party_model_saas` |
| `dvc-pipeline.yml` | `dvc repro` + `dvc push` | `1st_party_model` |

## Security Flags

| Component | Flag | Severity |
|---|---|---|
| `unsafe-serialization` | `pickle_load` | CRITICAL |
| `unsafe-serialization` | `torch_load_unsafe` | CRITICAL |
| `unsafe-serialization` | `joblib_load` | CRITICAL |
| `safe-serialization` | `safetensors_used` | INFO |
| `safe-serialization` | `torch_load_safe` | INFO |
| `safe-serialization` | `onnx_used` | INFO |

## Scanning

Point the AI-SPM scanner at this repo:

```bash
# Via API (direct repo scan)
curl -X POST http://localhost:8000/api/scans/github \
  -H "Content-Type: application/json" \
  -d '{"repos": ["<org>/myntra-ai-spm-test"]}'
```
