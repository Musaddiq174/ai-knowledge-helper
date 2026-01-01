"""
Embeddings Module
Generates semantic embeddings using SentenceTransformers
"""
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import logging
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance (loaded once)
_model = None


def load_embedding_model(model_name: str = None) -> SentenceTransformer:
    """
    Load the embedding model (singleton pattern).
    
    Args:
        model_name: Name of the model to load
        
    Returns:
        Loaded SentenceTransformer model
    """
    global _model
    
    if _model is None:
        model_name = model_name or config.EMBEDDING_MODEL
        logger.info(f"Loading embedding model: {model_name}")
        _model = SentenceTransformer(model_name)
        logger.info("Model loaded successfully")
    
    return _model


def create_embeddings(texts: List[str], model_name: str = None) -> Tuple[np.ndarray, List[str]]:
    """
    Create embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed
        model_name: Optional model name (uses config default if None)
        
    Returns:
        Tuple of (embeddings array, texts list)
    """
    if not texts:
        logger.warning("No texts provided for embedding")
        return np.array([]), []
    
    model = load_embedding_model(model_name)
    
    logger.info(f"Creating embeddings for {len(texts)} texts...")
    
    # Generate embeddings in batches for efficiency
    batch_size = 32
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(
            batch,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for cosine similarity
        )
        embeddings.append(batch_embeddings)
        logger.info(f"Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
    
    # Concatenate all embeddings
    all_embeddings = np.vstack(embeddings)
    
    logger.info(f"Created embeddings with shape: {all_embeddings.shape}")
    
    return all_embeddings, texts


def create_query_embedding(query: str, model_name: str = None) -> np.ndarray:
    """
    Create embedding for a single query.
    
    Args:
        query: Query text string
        model_name: Optional model name
        
    Returns:
        Query embedding as numpy array
    """
    model = load_embedding_model(model_name)
    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embedding


if __name__ == "__main__":
    # Test embeddings
    sample_texts = [
        "This is a sample document about artificial intelligence.",
        "Machine learning is a subset of AI.",
        "The weather today is sunny and warm."
    ]
    
    embeddings, texts = create_embeddings(sample_texts)
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Number of texts: {len(texts)}")
    
    # Test query embedding
    query = "What is artificial intelligence?"
    query_emb = create_query_embedding(query)
    print(f"Query embedding shape: {query_emb.shape}")

