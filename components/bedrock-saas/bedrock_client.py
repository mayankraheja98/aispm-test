"""AWS Bedrock runtime client for Claude."""
import json
import boto3

# Endpoint: bedrock-runtime.ap-south-1.amazonaws.com
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-south-1",
)

BEDROCK_ENDPOINT = "https://bedrock-runtime.ap-south-1.amazonaws.com"

body = json.dumps({
    "prompt": "\n\nHuman: What is the best ethnic wear for a wedding?\n\nAssistant:",
    "max_tokens_to_sample": 300,
})

response = client.invoke_model(
    body=body,
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    accept="application/json",
    contentType="application/json",
)
result = json.loads(response["body"].read())
print(result["completion"])
