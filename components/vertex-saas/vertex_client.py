"""Vertex AI (aiplatform.googleapis.com) and Gemini API consumers."""
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel

# Vertex endpoint: asia-south1-aiplatform.googleapis.com
vertexai.init(project="myntra-ai-prod", location="asia-south1")
VERTEX_ENDPOINT = "https://asia-south1-aiplatform.googleapis.com"

vertex_model = GenerativeModel("gemini-1.5-pro")
response = vertex_model.generate_content("Recommend sustainable fashion choices")
print(response.text)

# Gemini API: generativelanguage.googleapis.com
genai.configure(api_key="GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta"
gemini = genai.GenerativeModel("gemini-1.5-flash")
result = gemini.generate_content("List 5 trending Indian fashion styles")
print(result.text)
