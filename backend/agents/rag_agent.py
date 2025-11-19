# backend/agents/rag_agent.py

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Load local embedding model (FREE, offline)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB client (no deprecated config)
chroma_client = chromadb.Client(Settings(persist_directory="vector_store"))

# Create / load collection
collection = chroma_client.get_or_create_collection(
    name="research_docs",
    metadata={"hnsw:space": "cosine"}
)

# -------------------------
# Generate Embeddings
# -------------------------
def embed(text: str):
    return embedding_model.encode(text).tolist()

# -------------------------
# Store Document
# -------------------------
def store_document_in_vector_db(text: str, filename: str):
    vector = embed(text)

    collection.add(
        documents=[text],
        embeddings=[vector],
        ids=[filename]
    )

# -------------------------
# Query Vector DB
# -------------------------
def query_vector_db(question: str):
    question_embedding = embed(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    # If empty → return None
    if not results["documents"] or len(results["documents"][0]) == 0:
        return ""

    return results["documents"][0][0]
