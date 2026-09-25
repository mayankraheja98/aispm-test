"""HuggingFace Inference Endpoint (Dedicated) on AWS."""
import os
import requests

# Dedicated Inference Endpoint: *.aws.endpoints.huggingface.cloud
HF_ENDPOINT_URL = "https://xyz123abc.us-east-1.aws.endpoints.huggingface.cloud"
HF_TOKEN = os.environ["HUGGINGFACE_TOKEN"]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}
payload = {"inputs": "Describe this kurta:", "parameters": {"max_new_tokens": 100}}

response = requests.post(HF_ENDPOINT_URL, headers=headers, json=payload)
print(response.json())
