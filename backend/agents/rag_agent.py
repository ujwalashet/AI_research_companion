import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client(
    Settings(persist_directory="vector_store")
)

collection = chroma_client.get_or_create_collection(
    name="research_docs",
    metadata={"hnsw:space": "cosine"}
)

def embed(text: str):
    return embedding_model.encode(text).tolist()

def store_document_in_vector_db(text: str, filename: str):
    vector = embed(text)
    collection.add(
        documents=[text],
        embeddings=[vector],
        ids=[filename]
    )

def query_vector_db(question: str):
    question_embedding = embed(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    if not results["documents"]:
        return ""

    return results["documents"][0][0]
