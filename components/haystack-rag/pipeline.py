"""Haystack pipeline for fashion knowledge retrieval."""
from haystack import Document, Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

doc_store = InMemoryDocumentStore()
embedder = SentenceTransformersDocumentEmbedder(model="BAAI/bge-small-en-v1.5")
embedder.warm_up()

docs = [
    Document(content="Myntra offers 30-day hassle-free returns"),
    Document(content="Size charts are available on each product page"),
]
embedder.run(documents=docs)
doc_store.write_documents(docs)

retriever = InMemoryEmbeddingRetriever(document_store=doc_store)
prompt_builder = PromptBuilder(
    template="Answer using context:\n{% for doc in documents %}{{ doc.content }}\n{% endfor %}\nQuestion: {{ question }}"
)

pipeline = Pipeline()
pipeline.add_component("retriever", retriever)
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.connect("retriever.documents", "prompt_builder.documents")
result = pipeline.run({"retriever": {"query_embedding": []}, "prompt_builder": {"question": "What is the return window?"}})
