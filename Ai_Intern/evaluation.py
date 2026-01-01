"""
Evaluation Module
Evaluate retrieval quality and answer relevance
"""
import numpy as np
from typing import List, Tuple, Dict
import logging
from embeddings import create_query_embedding, create_embeddings
from retrieval import search_similar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_relevance_score(query: str, retrieved_texts: List[str]) -> float:
    """
    Calculate relevance score between query and retrieved texts.
    
    Args:
        query: User query
        retrieved_texts: List of retrieved text chunks
        
    Returns:
        Average relevance score (0-1)
    """
    if not retrieved_texts:
        return 0.0
    
    # Create embeddings
    query_emb = create_query_embedding(query)
    retrieved_embs, _ = create_embeddings(retrieved_texts)
    
    # Calculate cosine similarities
    similarities = []
    for emb in retrieved_embs:
        similarity = np.dot(query_emb, emb)  # Already normalized
        similarities.append(similarity)
    
    avg_similarity = np.mean(similarities)
    
    return float(avg_similarity)


def evaluate_retrieval(query: str, retrieved_texts: List[str], min_score: float = 0.6) -> Dict:
    """
    Evaluate if retrieved text matches the query intent.
    
    Args:
        query: User query
        retrieved_texts: List of retrieved text chunks
        min_score: Minimum relevance score threshold
        
    Returns:
        Dictionary with evaluation metrics
    """
    relevance_score = calculate_relevance_score(query, retrieved_texts)
    
    # Check coverage (simple keyword-based)
    query_keywords = set(word.lower() for word in query.split() if len(word) > 3)
    retrieved_text = " ".join(retrieved_texts).lower()
    
    covered_keywords = sum(1 for keyword in query_keywords if keyword in retrieved_text)
    coverage = covered_keywords / len(query_keywords) if query_keywords else 0.0
    
    # Overall assessment
    is_relevant = relevance_score >= min_score
    is_complete = coverage >= 0.5  # At least 50% keyword coverage
    
    evaluation = {
        "relevance_score": relevance_score,
        "coverage": coverage,
        "is_relevant": is_relevant,
        "is_complete": is_complete,
        "assessment": "Good" if (is_relevant and is_complete) else "Needs improvement"
    }
    
    return evaluation


def evaluate_answer_quality(answer: str, query: str, context: str) -> Dict:
    """
    Evaluate the quality of the generated answer.
    
    Args:
        answer: Generated answer
        context: Retrieved context used
        query: Original query
        
    Returns:
        Dictionary with quality metrics
    """
    # Check if answer is not empty
    has_answer = len(answer.strip()) > 0
    
    # Check if answer mentions context keywords
    context_keywords = set(word.lower() for word in context.split() if len(word) > 4)
    answer_lower = answer.lower()
    context_usage = sum(1 for keyword in context_keywords if keyword in answer_lower)
    context_usage_ratio = context_usage / len(context_keywords) if context_keywords else 0.0
    
    # Check answer length (not too short, not too long)
    answer_length = len(answer.split())
    length_score = 1.0 if 10 <= answer_length <= 200 else 0.5
    
    quality = {
        "has_answer": has_answer,
        "context_usage": context_usage_ratio,
        "length_score": length_score,
        "overall_quality": "Good" if (has_answer and context_usage_ratio > 0.3) else "Needs improvement"
    }
    
    return quality


def comprehensive_evaluation(query: str, retrieved_texts: List[str], answer: str) -> Dict:
    """
    Comprehensive evaluation of the entire RAG pipeline.
    
    Args:
        query: User query
        retrieved_texts: Retrieved text chunks
        answer: Generated answer
        
    Returns:
        Complete evaluation report
    """
    context = "\n\n".join(retrieved_texts)
    
    retrieval_eval = evaluate_retrieval(query, retrieved_texts)
    answer_eval = evaluate_answer_quality(answer, query, context)
    
    overall_score = (
        retrieval_eval["relevance_score"] * 0.5 +
        retrieval_eval["coverage"] * 0.2 +
        answer_eval["context_usage"] * 0.2 +
        answer_eval["length_score"] * 0.1
    )
    
    evaluation = {
        "query": query,
        "retrieval_evaluation": retrieval_eval,
        "answer_evaluation": answer_eval,
        "overall_score": overall_score,
        "recommendation": "Good" if overall_score >= 0.7 else "Needs improvement"
    }
    
    return evaluation


if __name__ == "__main__":
    # Test evaluation
    query = "What is artificial intelligence?"
    retrieved = [
        "Artificial intelligence is the simulation of human intelligence by machines.",
        "AI systems can learn and adapt from data."
    ]
    answer = "Artificial intelligence is the simulation of human intelligence by machines. AI systems can learn and adapt from data."
    
    eval_result = comprehensive_evaluation(query, retrieved, answer)
    print("Evaluation Results:")
    print(f"Relevance Score: {eval_result['retrieval_evaluation']['relevance_score']:.3f}")
    print(f"Coverage: {eval_result['retrieval_evaluation']['coverage']:.3f}")
    print(f"Overall Score: {eval_result['overall_score']:.3f}")
    print(f"Recommendation: {eval_result['recommendation']}")

