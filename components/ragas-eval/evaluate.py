"""RAGAS evaluation of the ChromaDB RAG pipeline."""
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset

# Test questions and reference answers
data = {
    "question": ["What is Myntra's return policy?", "How do I track my order?"],
    "answer": ["Myntra offers 30-day returns", "Use the My Orders section"],
    "contexts": [["Myntra's return window is 30 days from delivery"]],
    "ground_truth": ["30-day return policy"],
}
dataset = Dataset.from_dict(data)

result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(result)
