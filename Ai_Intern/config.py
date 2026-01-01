"""
Configuration file for AI Knowledge Helper RAG System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Alternative: "sentence-transformers/all-mpnet-base-v2" (better quality, slower)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"  # or "gpt-3.5-turbo" for faster/cheaper
USE_OPENAI = bool(OPENAI_API_KEY)  # Set to False to use local fallback

# Text Chunking Configuration
CHUNK_SIZE = 500  # Number of tokens per chunk
CHUNK_OVERLAP = 50  # Overlap between chunks (for context preservation)

# Retrieval Configuration
TOP_K = 3  # Number of chunks to retrieve for each query
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score for retrieval

# Vector Database Configuration
VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "documents"

# Data Directory
DATA_DIR = "data"

# LLM Prompt Template
PROMPT_TEMPLATE = """You are a helpful AI assistant that answers questions based on the provided context.

Context:
{context}

Question: {question}

Please provide a clear and concise answer based only on the context provided. If the context doesn't contain enough information to answer the question, say so.

Answer:"""

# Evaluation Configuration
EVALUATION_ENABLED = True
MIN_RELEVANCE_SCORE = 0.6  # Minimum relevance score for evaluation

