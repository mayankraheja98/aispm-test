# Myntra AI-SPM Test Repo

> **Purpose:** This is a dummy repository containing realistic example code for every AI asset type detectable by the AI-SPM scanner. It is used to validate the scanner's classification engine end-to-end.

## What This Repo Covers

| Directory | Asset Type | Detection Signals |
|---|---|---|
| `server.py` (root) | **MCP Server** | `from mcp import Server`, `@server.tool()`, `StdioServerTransport` |
| `agent.py` (root) | **AI Agent (1st Party)** | `AgentExecutor`, `create_react_agent`, `langchain`, `langgraph` |
| `train.py` (root) | **1st Party Model** | `trainer.train()`, `loss.backward()`, `torch`, `transformers`, `DataLoader` |
| `app.py` (root) | **3rd Party Model (SaaS)** | `anthropic.Anthropic()`, `openai.OpenAI()`, `cohere.Client()` |
| `pipeline.py` (root) | **AI Pipeline** | `prefect`, `@flow`, `@task`, `langchain chain` |
| `mcp_server/` | MCP Server (detailed) | Full MCP server implementation |
| `langchain_agent/` | Agent (LangChain) | LangChain + LangGraph customer service agent |
| `adk_agent/` | Agent (Google ADK) | Google ADK pricing optimization agent |
| `crewai_agent/` | Agent (CrewAI) | Multi-agent trend analysis crew |
| `model_training/` | 1st Party Model | LoRA fine-tuning pipeline |
| `saas_consumer/` | 3rd Party Model (SaaS) | OpenAI / Anthropic / Cohere API consumption |
| `self_hosted_llm/` | 3rd Party Model (Hosted) | Ollama + llama.cpp on-prem inference |
| `ai_pipeline/` | AI Pipeline | Prefect + LangChain daily enrichment pipeline |
| `mcp_client/` | MCP Client | `claude_desktop_config.json` |
| `skill_plugin/` | Skill / Plugin | `SKILL.md` + Anthropic tool use |
| `.mcp.json` (root) | MCP Client | Root-level MCP client config |
| `SKILL.md` (root) | Skill / Plugin | Root-level skill manifest |

## Dependency Coverage (root requirements.txt)

The root `requirements.txt` intentionally contains all AI framework dependencies
so the scanner can detect every asset type from a single repository scan.

```
mcp                           → MCP Server/Client
langchain, langgraph          → AI Agent (LangChain)
google-adk                    → AI Agent (Google ADK)
crewai, autogen, pydantic-ai  → AI Agent (various)
torch, transformers, peft     → 1st Party Model training
openai, anthropic, cohere     → 3rd Party Model (SaaS)
llama-cpp-python, ollama      → 3rd Party Model (Hosted)
prefect                       → AI Pipeline
```

## How the Scanner Finds This Repo

The AI-SPM GitHub scanner will find this repo via code search queries like:
- `org:<your-org> openai OR anthropic OR langchain in:file filename:requirements.txt`
- `org:<your-org> @modelcontextprotocol/sdk in:file filename:package.json`
- `org:<your-org> from mcp import in:file extension:py`

Then it will:
1. Fetch `requirements.txt` and `package.json` → extract all dependency signals
2. Sample root-level code files (`server.py`, `agent.py`, `train.py`, `app.py`, `pipeline.py`) → match code patterns
3. Check for `SKILL.md` and `.mcp.json` in the file tree
4. Run classifier → outputs `mcp_server` as primary type (highest priority), with all other types in `asset_types_all`

## Expected Scanner Output

```json
{
  "id": "GH-<your-org>/myntra-ai-spm-test",
  "name": "myntra-ai-spm-test",
  "asset_type": "mcp_server",
  "frameworks": ["mcp", "langchain", "openai", "anthropic", "torch", "crewai", ...],
  "classification_signals": {
    "mcp_server": { "libs": ["mcp"], "code_match": true },
    "ai_agent_1st_party": { "libs": ["langchain", "crewai", "google-adk"], "code_match": true },
    "1st_party_model": { "libs": ["torch", "transformers"], "code_match": true },
    "3rd_party_model_saas": { "libs": ["openai", "anthropic", "cohere"] },
    "3rd_party_model_hosted": { "libs": ["llama-cpp-python", "ollama"] },
    "skill_plugin": { "skill_file": true },
    "mcp_client": { "config_files": true },
    "ai_pipeline": { "libs": ["prefect"] }
  },
  "raw_metadata": {
    "asset_types_all": ["mcp_server", "ai_agent_1st_party", "1st_party_model",
                        "3rd_party_model_saas", "3rd_party_model_hosted",
                        "skill_plugin", "mcp_client", "ai_pipeline"]
  }
}
```

## ⚠️ Not for Production Use

All API keys in this repo are placeholder strings. No real credentials are included.
This repo is purely for scanner validation and should be kept private within your GitHub org.
