"""
Retrieval Module
Vector database setup and similarity search using ChromaDB
"""
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Tuple
import logging
import config
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global client and collection
_client = None
_collection = None


def setup_vector_db(embeddings: np.ndarray, texts: List[str], collection_name: str = None) -> chromadb.Collection:
    """
    Set up ChromaDB vector database with embeddings and texts.
    
    Args:
        embeddings: Numpy array of embeddings
        texts: List of corresponding text chunks
        collection_name: Name for the collection
        
    Returns:
        ChromaDB collection object
    """
    global _client, _collection
    
    collection_name = collection_name or config.COLLECTION_NAME
    
    # Create or get client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=config.VECTOR_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        logger.info(f"Initialized ChromaDB client at {config.VECTOR_DB_PATH}")
    
    # Delete existing collection if it exists (for fresh start)
    try:
        _client.delete_collection(collection_name)
        logger.info(f"Deleted existing collection: {collection_name}")
    except:
        pass
    
    # Create or get collection
    _collection = _client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    
    # Add documents to collection
    # ChromaDB expects embeddings as lists
    embeddings_list = embeddings.tolist()
    
    # Create IDs for each document
    ids = [f"doc_{i}" for i in range(len(texts))]
    
    # Add to collection
    _collection.add(
        embeddings=embeddings_list,
        documents=texts,
        ids=ids
    )
    
    logger.info(f"Added {len(texts)} documents to collection '{collection_name}'")
    
    return _collection


def load_vector_db(collection_name: str = None) -> chromadb.Collection:
    """
    Load existing vector database collection.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        ChromaDB collection object
    """
    global _client, _collection
    
    collection_name = collection_name or config.COLLECTION_NAME
    
    if _client is None:
        _client = chromadb.PersistentClient(
            path=config.VECTOR_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
    
    try:
        _collection = _client.get_collection(collection_name)
        logger.info(f"Loaded existing collection: {collection_name}")
        return _collection
    except Exception as e:
        logger.error(f"Collection not found: {e}")
        return None


def search_similar(query_embedding: np.ndarray, top_k: int = None) -> List[Tuple[str, float]]:
    """
    Search for similar documents using query embedding.
    
    Args:
        query_embedding: Query embedding vector
        top_k: Number of results to return
        
    Returns:
        List of tuples (text, similarity_score)
    """
    global _collection
    
    if _collection is None:
        _collection = load_vector_db()
    
    if _collection is None:
        logger.error("Vector database not initialized. Please run setup_vector_db first.")
        return []
    
    top_k = top_k or config.TOP_K
    
    # Convert embedding to list
    query_embedding_list = query_embedding.tolist()
    
    # Search
    results = _collection.query(
        query_embeddings=[query_embedding_list],
        n_results=top_k
    )
    
    # Extract documents and distances
    documents = results['documents'][0] if results['documents'] else []
    distances = results['distances'][0] if results['distances'] else []
    
    # Convert distances to similarity scores (1 - distance for cosine)
    similarities = [(doc, 1 - dist) for doc, dist in zip(documents, distances)]
    
    # Filter by similarity threshold
    similarities = [(doc, sim) for doc, sim in similarities if sim >= config.SIMILARITY_THRESHOLD]
    
    logger.info(f"Retrieved {len(similarities)} documents (top_k={top_k})")
    
    return similarities


if __name__ == "__main__":
    # Test retrieval (requires embeddings to be created first)
    from embeddings import create_embeddings, create_query_embedding
    
    sample_texts = [
        "Artificial intelligence is transforming the world.",
        "Machine learning algorithms learn from data.",
        "The weather forecast predicts rain tomorrow."
    ]
    
    # Create embeddings and setup DB
    embeddings, texts = create_embeddings(sample_texts)
    collection = setup_vector_db(embeddings, texts)
    
    # Test search
    query = "What is AI?"
    query_emb = create_query_embedding(query)
    results = search_similar(query_emb, top_k=2)
    
    print(f"\nQuery: {query}")
    print("\nRetrieved documents:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"{i}. (similarity: {score:.3f}) {doc[:100]}...")

