"""ChromaDB-backed RAG for Myntra fashion Q&A."""
import chromadb
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Build vector store
client = chromadb.PersistentClient(path="./chroma_db")
embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    client=client,
    collection_name="myntra-catalogue",
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Build RAG chain
llm = ChatOpenAI(model="gpt-4o-mini")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

def answer(question: str) -> str:
    docs = retriever.invoke(question)
    result = qa_chain.invoke({"query": question})
    return result["result"]
