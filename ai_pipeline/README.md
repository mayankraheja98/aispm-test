# Myntra AI Catalog Enrichment Pipeline
Daily Prefect pipeline that enriches new product listings with AI-generated
descriptions, semantic embeddings, and relevance scores.

**Asset type:** AI Pipeline
**Orchestrator:** Prefect (self-hosted on AKS)
**Schedule:** Daily at 02:00 IST
**Steps:** Extract → AI Describe (GPT-4o-mini) → Embed (Cohere) → Score (1P model) → Load (Elasticsearch)
