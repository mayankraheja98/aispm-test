"""Azure AI Foundry (services.ai.azure.com) and Managed Inference endpoint."""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Azure AI Foundry endpoint
FOUNDRY_ENDPOINT = "https://myntra-hub.services.ai.azure.com"

# Azure ML managed online endpoint
ML_ENDPOINT = "https://my-llama-endpoint.eastus.inference.ml.azure.com"

foundry_client = ChatCompletionsClient(
    endpoint=FOUNDRY_ENDPOINT,
    credential=AzureKeyCredential(os.environ["AZURE_AI_KEY"]),
)

response = foundry_client.complete(
    messages=[{"role": "user", "content": "Describe fashion trends"}],
    model="Phi-3-medium-128k-instruct",
)
print(response.choices[0].message.content)
