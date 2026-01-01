"""
Example Usage Script
Demonstrates how to use the AI Knowledge Helper RAG system
"""
from qa_pipeline import RAGPipeline
from evaluation import comprehensive_evaluation

def main():
    print("=" * 60)
    print("AI Knowledge Helper - Example Usage")
    print("=" * 60)
    
    # Initialize RAG pipeline
    print("\n1. Initializing RAG pipeline...")
    rag = RAGPipeline()
    
    # Process documents (if not already processed)
    if not rag.vector_db_loaded:
        print("\n2. Processing documents...")
        print("   (This may take a few minutes for the first time)")
        rag.process_documents("data", force_rebuild=False)
    else:
        print("\n2. Vector database already loaded!")
    
    # Example questions
    questions = [
        "What is the main topic of the document?",
        "Can you summarize the key points?",
        "What are the important concepts discussed?"
    ]
    
    print("\n3. Asking questions...")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("-" * 60)
        
        # Get answer
        result = rag.ask(question, use_summarization=False)
        
        print(f"Answer: {result['answer']}")
        print(f"\nConfidence: {result['confidence']:.3f}")
        print(f"Sources: {result['num_sources']}")
        
        # Evaluate (optional)
        if result.get("sources"):
            eval_result = comprehensive_evaluation(
                query=question,
                retrieved_texts=result["sources"],
                answer=result["answer"]
            )
            print(f"Overall Score: {eval_result['overall_score']:.3f}")
        
        print("\n" + "=" * 60)
    
    print("\n Example usage complete!")
    print("\nTo use the FastAPI server, run: python main.py")
    print("To use the Jupyter notebook, run: jupyter notebook")

if __name__ == "__main__":
    main()

