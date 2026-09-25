"""FAISS-backed retrieval for product search."""
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings = OpenAIEmbeddings()

def build_index(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def load_and_query(question: str) -> str:
    vectorstore = FAISS.load_local("faiss_index", embeddings)
    docs = vectorstore.similarity_search(question, k=4)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain.invoke({"query": question})["result"]
