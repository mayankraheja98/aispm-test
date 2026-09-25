"""Databricks Foundation Model API via *.cloud.databricks.com endpoint."""
import os
from openai import OpenAI

# Databricks workspace endpoint
DATABRICKS_HOST = "https://myntra.cloud.databricks.com"
DATABRICKS_TOKEN = os.environ["DATABRICKS_TOKEN"]

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url=f"{DATABRICKS_HOST}/serving-endpoints",
)

response = client.chat.completions.create(
    model="databricks-meta-llama-3-1-70b-instruct",
    messages=[{"role": "user", "content": "Describe Myntra's fashion categories"}],
)
print(response.choices[0].message.content)
