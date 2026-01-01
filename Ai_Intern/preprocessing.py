"""
Text Preprocessing Module
Cleans and chunks text documents for optimal retrieval
"""
import re
import tiktoken
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize tokenizer
try:
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
except:
    encoding = None
    logger.warning("tiktoken not available, using character-based chunking")


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def count_tokens(text: str) -> int:
    """
    Count tokens in text (approximate if tiktoken not available).
    
    Args:
        text: Text string
        
    Returns:
        Number of tokens (approximate)
    """
    if encoding:
        return len(encoding.encode(text))
    else:
        # Fallback: approximate 1 token = 4 characters
        return len(text) // 4


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Split text into chunks with overlap.
    
    Args:
        text: Text to chunk
        chunk_size: Target number of tokens per chunk
        chunk_overlap: Number of tokens to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Clean the text first
    text = clean_text(text)
    
    if not text:
        return []
    
    # Split by sentences first (better chunking)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sentence_tokens = count_tokens(sentence)
        
        # If single sentence is larger than chunk_size, split it
        if sentence_tokens > chunk_size:
            # Add current chunk if exists
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split large sentence by words
            words = sentence.split()
            temp_chunk = []
            temp_size = 0
            
            for word in words:
                word_tokens = count_tokens(word)
                if temp_size + word_tokens > chunk_size and temp_chunk:
                    chunks.append(" ".join(temp_chunk))
                    # Start new chunk with overlap
                    overlap_words = temp_chunk[-chunk_overlap:] if len(temp_chunk) > chunk_overlap else temp_chunk
                    temp_chunk = overlap_words + [word]
                    temp_size = count_tokens(" ".join(temp_chunk))
                else:
                    temp_chunk.append(word)
                    temp_size += word_tokens
            
            if temp_chunk:
                current_chunk = temp_chunk
                current_size = temp_size
        else:
            # Check if adding this sentence would exceed chunk size
            if current_size + sentence_tokens > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                
                # Start new chunk with overlap from previous
                overlap_text = " ".join(current_chunk[-chunk_overlap:]) if len(current_chunk) > chunk_overlap else " ".join(current_chunk)
                current_chunk = [overlap_text, sentence] if overlap_text else [sentence]
                current_size = count_tokens(" ".join(current_chunk))
            else:
                current_chunk.append(sentence)
                current_size += sentence_tokens
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    # Filter out very small chunks
    chunks = [chunk for chunk in chunks if count_tokens(chunk) > 10]
    
    logger.info(f"Created {len(chunks)} chunks from text (avg size: {sum(count_tokens(c) for c in chunks) // len(chunks) if chunks else 0} tokens)")
    
    return chunks


def preprocess_text(texts: List[str], chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Preprocess a list of texts: clean and chunk.
    
    Args:
        texts: List of raw text strings
        chunk_size: Target number of tokens per chunk
        chunk_overlap: Number of tokens to overlap between chunks
        
    Returns:
        List of processed text chunks
    """
    all_chunks = []
    
    for i, text in enumerate(texts):
        chunks = chunk_text(text, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
        logger.info(f"Processed document {i+1}/{len(texts)}: {len(chunks)} chunks")
    
    logger.info(f"Total chunks created: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    # Test preprocessing
    sample_text = """
    This is a sample document. It contains multiple sentences. 
    Each sentence should be properly chunked. The chunking process 
    should preserve context. Overlapping chunks help maintain continuity.
    This is important for retrieval. The system needs to understand context.
    """
    
    chunks = chunk_text(sample_text, chunk_size=50, chunk_overlap=10)
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({count_tokens(chunk)} tokens):")
        print(chunk[:100] + "..." if len(chunk) > 100 else chunk)

