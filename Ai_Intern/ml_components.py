"""
ML Components Module
Optional ML features: summarization, question classification
"""
import logging
from typing import List, Dict
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def summarize_chunks(chunks: List[str], max_length: int = 150) -> str:
    """
    Summarize a list of text chunks.
    
    Args:
        chunks: List of text chunks to summarize
        max_length: Maximum length of summary
        
    Returns:
        Summarized text
    """
    if not chunks:
        return ""
    
    # Simple extractive summarization: take first sentences from each chunk
    summary_sentences = []
    total_length = 0
    
    for chunk in chunks:
        sentences = chunk.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 20:  # Filter very short sentences
                if total_length + len(sentence) <= max_length:
                    summary_sentences.append(sentence)
                    total_length += len(sentence)
                else:
                    break
        if total_length >= max_length:
            break
    
    summary = ". ".join(summary_sentences)
    if summary and not summary.endswith('.'):
        summary += "."
    
    logger.info(f"Summarized {len(chunks)} chunks into {len(summary)} characters")
    
    return summary


def classify_question_type(question: str) -> str:
    """
    Classify the type of question.
    
    Args:
        question: User question
        
    Returns:
        Question type (factual, analytical, comparative, etc.)
    """
    question_lower = question.lower()
    
    # Factual questions (what, who, when, where)
    if any(word in question_lower for word in ["what is", "who is", "when", "where", "what are"]):
        return "factual"
    
    # Analytical questions (how, why)
    elif any(word in question_lower for word in ["how", "why"]):
        return "analytical"
    
    # Comparative questions
    elif any(word in question_lower for word in ["compare", "difference", "versus", "vs", "better"]):
        return "comparative"
    
    # Opinion questions
    elif any(word in question_lower for word in ["opinion", "think", "believe", "should"]):
        return "opinion"
    
    # Yes/No questions
    elif question_lower.strip().startswith(("is ", "are ", "can ", "do ", "does ", "did ")):
        return "yes_no"
    
    else:
        return "general"


def get_question_specific_prompt(question: str, context: str) -> str:
    """
    Get a prompt tailored to the question type.
    
    Args:
        question: User question
        context: Retrieved context
        
    Returns:
        Tailored prompt
    """
    question_type = classify_question_type(question)
    
    base_prompt = config.PROMPT_TEMPLATE.format(context=context, question=question)
    
    type_specific_instructions = {
        "factual": "Provide a clear, factual answer based on the context.",
        "analytical": "Explain the reasoning and provide a detailed analysis.",
        "comparative": "Compare and contrast the relevant information.",
        "opinion": "Present the information objectively, noting it's based on the provided context.",
        "yes_no": "Provide a clear yes or no answer, followed by explanation.",
        "general": "Provide a comprehensive answer based on the context."
    }
    
    instruction = type_specific_instructions.get(question_type, "")
    
    if instruction:
        return base_prompt + f"\n\nNote: {instruction}"
    
    return base_prompt


def cluster_documents(embeddings, n_clusters: int = 5) -> Dict:
    """
    Cluster documents to improve RAG retrieval.
    
    Args:
        embeddings: Document embeddings
        n_clusters: Number of clusters
        
    Returns:
        Dictionary with cluster assignments
    """
    try:
        from sklearn.cluster import KMeans
        import numpy as np
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
        
        logger.info(f"Clustered {len(embeddings)} documents into {n_clusters} clusters")
        
        return {
            "clusters": clusters,
            "labels": cluster_labels.tolist(),
            "centroids": kmeans.cluster_centers_.tolist()
        }
    
    except ImportError:
        logger.warning("scikit-learn not available. Install with: pip install scikit-learn")
        return {"error": "scikit-learn not installed"}


if __name__ == "__main__":
    # Test summarization
    chunks = [
        "Artificial intelligence is transforming many industries. Machine learning algorithms can process vast amounts of data.",
        "Natural language processing enables computers to understand human language. This technology powers chatbots and virtual assistants."
    ]
    
    summary = summarize_chunks(chunks)
    print("Summary:", summary)
    
    # Test question classification
    questions = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Compare AI and traditional programming.",
        "Is AI better than human intelligence?"
    ]
    
    for q in questions:
        q_type = classify_question_type(q)
        print(f"Question: {q}")
        print(f"Type: {q_type}\n")

