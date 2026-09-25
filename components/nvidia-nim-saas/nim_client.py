"""Nvidia NIM (NVCF) API client."""
import os
from openai import OpenAI

# Nvidia NIM endpoint
NIM_ENDPOINT = "https://integrate.api.nvidia.com/v1"
NVCF_ENDPOINT = "https://nvcf.api.nvidia.com/v2/nvcf/pexec/functions"
NVIDIA_API_KEY = os.environ["NVIDIA_API_KEY"]

client = OpenAI(
    base_url=NIM_ENDPOINT,
    api_key=NVIDIA_API_KEY,
)

response = client.chat.completions.create(
    model="meta/llama-3.1-70b-instruct",
    messages=[{"role": "user", "content": "Suggest a summer fashion palette"}],
)
print(response.choices[0].message.content)
