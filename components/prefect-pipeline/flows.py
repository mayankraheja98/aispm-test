"""Prefect flow: daily AI-powered catalogue enrichment pipeline."""
from prefect import flow, task
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd

llm = ChatOpenAI(model="gpt-4o-mini")

@task(retries=2)
def extract_new_products() -> pd.DataFrame:
    """Pull new products from catalogue DB."""
    return pd.DataFrame({"product_id": ["P001"], "title": ["Blue Kurta"]})

@task
def enrich_with_ai(df: pd.DataFrame) -> pd.DataFrame:
    """Generate AI descriptions for each product."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a fashion copywriter."),
        ("human", "Write a 50-word description for: {title}"),
    ])
    chain = prompt | llm
    df["description"] = df["title"].apply(
        lambda t: chain.invoke({"title": t}).content
    )
    return df

@task
def load_to_catalogue(df: pd.DataFrame) -> None:
    """Write enriched products back to catalogue."""
    df.to_csv("enriched_products.csv", index=False)

@flow(name="catalogue-enrichment", log_prints=True)
def catalogue_enrichment_flow():
    products = extract_new_products()
    enriched = enrich_with_ai(products)
    load_to_catalogue(enriched)

if __name__ == "__main__":
    catalogue_enrichment_flow()
