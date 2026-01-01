"""
RAG Pipeline Module
Complete question-answering pipeline: retrieval + LLM reasoning
"""
import os
from typing import Dict, List, Optional
import logging
import config
from embeddings import create_query_embedding, load_embedding_model
from retrieval import setup_vector_db, load_vector_db, search_similar
# Imports are done inside methods to avoid circular dependencies
from ml_components import summarize_chunks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Complete RAG pipeline for question answering.
    """
    
    def __init__(self):
        """Initialize the RAG pipeline."""
        self.vector_db_loaded = False
        self._ensure_vector_db()
    
    def _ensure_vector_db(self):
        """Check if vector DB exists, load if available."""
        collection = load_vector_db()
        if collection:
            self.vector_db_loaded = True
            logger.info("Vector database loaded successfully")
        else:
            logger.info("Vector database not found. Run process_documents() first.")
    
    def process_documents(self, data_dir: str = "data", force_rebuild: bool = False):
        """
        Process documents: ingest, preprocess, embed, and store in vector DB.
        
        Args:
            data_dir: Directory containing PDF files
            force_rebuild: If True, rebuild vector DB even if it exists
        """
        if self.vector_db_loaded and not force_rebuild:
            logger.info("Vector database already exists. Use force_rebuild=True to rebuild.")
            return
        
        logger.info("Starting document processing pipeline...")
        
        # Step 1: Ingest PDFs
        logger.info("Step 1: Ingesting PDFs...")
        from data_ingestion import ingest_pdfs as ingest
        texts = ingest(data_dir)
        
        if not texts:
            logger.error("No documents found. Please add PDF files to the data directory.")
            return
        
        # Step 2: Preprocess (chunk)
        logger.info("Step 2: Preprocessing and chunking...")
        from preprocessing import preprocess_text as preprocess
        chunks = preprocess(
            texts,
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
        # Step 3: Create embeddings
        logger.info("Step 3: Creating embeddings...")
        from embeddings import create_embeddings as create_emb
        embeddings, chunks = create_emb(chunks)
        
        # Step 4: Setup vector database
        logger.info("Step 4: Setting up vector database...")
        setup_vector_db(embeddings, chunks)
        self.vector_db_loaded = True
        
        logger.info("Document processing complete!")
    
    def _get_llm_response(self, context: str, question: str) -> str:
        """
        Get LLM response using OpenAI or fallback.
        
        Args:
            context: Retrieved context text
            question: User question
            
        Returns:
            LLM-generated answer
        """
        prompt = config.PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )
        
        if config.USE_OPENAI and config.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=config.OPENAI_API_KEY)
                
                response = client.chat.completions.create(
                    model=config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                return response.choices[0].message.content.strip()
            
            except Exception as e:
                logger.warning(f"OpenAI API error: {e}. Using fallback response.")
        
        # Fallback: Simple template-based response
        return self._fallback_response(context, question)
    
    def _fallback_response(self, context: str, question: str) -> str:
        """
        Fallback response when LLM is not available.
        
        Args:
            context: Retrieved context text
            question: User question
            
        Returns:
            Simple answer based on context
        """
        # Simple keyword-based answer
        question_lower = question.lower()
        context_lower = context.lower()
        
        # Find sentences that might answer the question
        sentences = context.split('.')
        relevant_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Check if sentence contains question keywords
            question_words = [w for w in question_lower.split() if len(w) > 3]
            if any(word in sentence_lower for word in question_words):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            return ". ".join(relevant_sentences[:2]) + "."
        else:
            return f"Based on the provided context: {context[:200]}..."
    
    def ask(self, question: str, top_k: int = None, use_summarization: bool = False) -> Dict:
        """
        Ask a question and get an answer using RAG.
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            use_summarization: Whether to summarize retrieved chunks
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        if not self.vector_db_loaded:
            logger.error("Vector database not loaded. Run process_documents() first.")
            return {
                "answer": "Error: Vector database not initialized.",
                "sources": [],
                "confidence": 0.0,
                "num_sources": 0
            }
        
        top_k = top_k or config.TOP_K
        
        # Step 1: Create query embedding
        logger.info(f"Processing question: {question}")
        query_embedding = create_query_embedding(question)
        
        # Step 2: Retrieve similar chunks
        logger.info("Retrieving relevant documents...")
        retrieved = search_similar(query_embedding, top_k=top_k)
        
        if not retrieved:
            return {
                "answer": "I couldn't find relevant information to answer your question.",
                "sources": [],
                "confidence": 0.0,
                "num_sources": 0
            }
        
        # Step 3: Prepare context
        sources = [doc for doc, score in retrieved]
        context = "\n\n".join(sources)
        
        # Optional: Summarize chunks
        if use_summarization:
            logger.info("Summarizing retrieved chunks...")
            context = summarize_chunks(sources)
        
        # Step 4: Generate answer using LLM
        logger.info("Generating answer...")
        answer = self._get_llm_response(context, question)
        
        # Calculate average confidence
        avg_confidence = sum(score for _, score in retrieved) / len(retrieved) if retrieved else 0.0
        
        result = {
            "answer": answer,
            "sources": sources[:3],  # Return top 3 sources
            "confidence": avg_confidence,
            "num_sources": len(retrieved)
        }
        
        logger.info(f"Answer generated (confidence: {avg_confidence:.2f})")
        
        return result


if __name__ == "__main__":
    # Test the pipeline
    rag = RAGPipeline()
    
    # Process documents (first time)
    # rag.process_documents("data")
    
    # Ask a question
    # result = rag.ask("What is the main topic?")
    # print("\nAnswer:", result["answer"])
    # print("\nConfidence:", result["confidence"])
    pass

