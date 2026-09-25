"""LlamaIndex RAG over Myntra catalogue documents."""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

Settings.chunk_size = 512
Settings.chunk_overlap = 50

qd_client = qdrant_client.QdrantClient(host="localhost", port=6333)
vector_store = QdrantVectorStore(client=qd_client, collection_name="myntra-docs")

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
query_engine = RetrieverQueryEngine(retriever=retriever)

response = query_engine.query("What is Myntra's return policy?")
print(response)
