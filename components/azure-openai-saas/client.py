"""Azure OpenAI Service client."""
import os
from openai import AzureOpenAI

# Endpoint: myntra-ai.openai.azure.com
AZURE_ENDPOINT = "https://myntra-ai.openai.azure.com"
DEPLOYMENT = "gpt-4o"

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01",
)

response = client.chat.completions.create(
    model=DEPLOYMENT,
    messages=[{"role": "user", "content": "Suggest ethnic wear for festive season"}],
)
print(response.choices[0].message.content)
