"""
AI Pipeline — Myntra Daily ML Workflow
Detection signals: prefect flow, langchain chain, DataLoader, training orchestration
Asset type: ai_pipeline
"""
import os
from datetime import datetime
from typing import Optional

from prefect import flow, task, get_run_logger
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain


# ── Tasks ──────────────────────────────────────────────────────────────────────

@task(retries=3, retry_delay_seconds=60)
def extract_catalog_data(date: str) -> list[dict]:
    """Pull new/updated product listings from catalog DB."""
    logger = get_run_logger()
    logger.info(f"Extracting catalog data for {date}")
    # Production: BigQuery query for delta catalog records
    return [{"product_id": "P001", "name": "Blue Kurta", "category": "Women"}]


@task
def generate_descriptions(products: list[dict]) -> list[dict]:
    """Batch-generate product descriptions using LangChain chain."""
    logger = get_run_logger()
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You write concise, appealing product descriptions for fashion e-commerce."),
        ("human", "Write a 2-sentence description for: {product_name} in category {category}"),
    ])
    chain = prompt | llm | StrOutputParser()

    enriched = []
    for product in products:
        logger.info(f"Generating description for {product['product_id']}")
        description = chain.invoke({
            "product_name": product["name"],
            "category": product["category"],
        })
        enriched.append({**product, "ai_description": description})

    logger.info(f"Generated descriptions for {len(enriched)} products")
    return enriched


@task
def generate_embeddings(products: list[dict]) -> list[dict]:
    """Generate semantic search embeddings via Cohere."""
    import cohere
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

    texts = [f"{p['name']} {p.get('ai_description', '')}" for p in products]
    response = co.embed(texts=texts, model="embed-english-v3.0", input_type="search_document")

    for i, product in enumerate(products):
        product["embedding"] = response.embeddings[i]
    return products


@task
def run_model_inference(products: list[dict]) -> list[dict]:
    """Run internal style recommender model for relevance scoring."""
    import torch
    # Production: loads from model registry (MLflow/Vertex AI)
    # Here: dummy scoring
    for product in products:
        product["relevance_score"] = 0.85
        product["style_cluster"] = "casual_summer"
    return products


@task
def load_to_search_index(products: list[dict], index_name: str = "myntra-products") -> dict:
    """Load enriched products into Elasticsearch/OpenSearch."""
    logger = get_run_logger()
    logger.info(f"Loading {len(products)} products to index '{index_name}'")
    # Production: bulk index via ES client
    return {"indexed": len(products), "index": index_name, "status": "success"}


@task
def notify_on_completion(result: dict, run_date: str):
    """Post pipeline completion summary to Slack."""
    logger = get_run_logger()
    logger.info(f"Pipeline complete for {run_date}: {result}")
    # Production: Slack webhook notification


# ── Flows ──────────────────────────────────────────────────────────────────────

@flow(name="myntra-catalog-enrichment", log_prints=True)
def catalog_enrichment_pipeline(run_date: Optional[str] = None):
    """
    Daily pipeline: Extract → AI Enrich → Embed → Score → Load to Search Index
    Runs every day at 2am IST to process new/updated catalog listings.
    """
    run_date = run_date or datetime.utcnow().strftime("%Y-%m-%d")
    logger = get_run_logger()
    logger.info(f"Starting catalog enrichment pipeline for {run_date}")

    # Step 1: Extract
    products = extract_catalog_data(run_date)

    # Step 2: AI enrichment (parallel)
    products_with_desc = generate_descriptions(products)
    products_with_embeddings = generate_embeddings(products_with_desc)

    # Step 3: Internal model scoring
    products_scored = run_model_inference(products_with_embeddings)

    # Step 4: Load
    result = load_to_search_index(products_scored)

    # Step 5: Notify
    notify_on_completion(result, run_date)

    return result


@flow(name="myntra-model-retraining-trigger")
def retraining_trigger_flow():
    """
    Weekly check: if model performance degrades below threshold, trigger retraining job.
    Triggered by Prefect schedule every Monday 6am IST.
    """
    logger = get_run_logger()
    # Production: fetch metrics from monitoring → compare to threshold
    current_ndcg = 0.82
    threshold = 0.80

    if current_ndcg < threshold:
        logger.warning(f"Model NDCG {current_ndcg} below threshold {threshold}. Triggering retrain.")
        # Production: submit Vertex AI / AKS training job
    else:
        logger.info(f"Model performance OK: NDCG={current_ndcg}")


if __name__ == "__main__":
    catalog_enrichment_pipeline()
