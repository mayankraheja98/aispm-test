"""IBM WatsonX.ai inference client."""
import os
from ibm_watsonx_ai import APIClient, Credentials

WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
WATSONX_API_KEY = os.environ["WATSONX_API_KEY"]

credentials = Credentials(url=WATSONX_URL, api_key=WATSONX_API_KEY)
client = APIClient(credentials=credentials)

params = {
    "model_id": "ibm/granite-13b-chat-v2",
    "input": "Recommend ethnic wear for office",
    "parameters": {"max_new_tokens": 200},
    "project_id": "myntra-ai-project",
}
response = client.foundation_models.generate_text(**params)
print(response)
