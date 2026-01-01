"""
Interactive Question-Answering Script
Easy-to-use interface for uploading documents and asking questions
"""
import os
import sys
from pathlib import Path

def print_header():
    print("\n" + "=" * 70)
    print("  AI KNOWLEDGE HELPER - Interactive Q&A System")
    print("=" * 70)

def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        import sentence_transformers
    except ImportError:
        missing.append("sentence-transformers")
    
    try:
        import chromadb
    except ImportError:
        missing.append("chromadb")
    
    try:
        import pypdf
    except ImportError:
        missing.append("pypdf")
    
    if missing:
        print("\n  Missing dependencies. Please install them first:")
        print(f"   pip install {' '.join(missing)}")
        print("\n   Or install all dependencies:")
        print("   pip install -r requirements.txt")
        return False
    return True

def show_menu():
    """Display main menu."""
    print("\n" + "-" * 70)
    print("MAIN MENU")
    print("-" * 70)
    print("1. Upload/Process PDF documents")
    print("2. Ask a question")
    print("3. View processed documents")
    print("4. Exit")
    print("-" * 70)

def upload_documents():
    """Guide user to upload documents."""
    print("\n" + "=" * 70)
    print("  UPLOAD DOCUMENTS")
    print("=" * 70)
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Check existing PDFs
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"\n Found {len(pdf_files)} PDF file(s) in data/ directory:")
        for i, pdf in enumerate(pdf_files, 1):
            size_kb = pdf.stat().st_size / 1024
            print(f"   {i}. {pdf.name} ({size_kb:.1f} KB)")
    else:
        print("\n No PDF files found in data/ directory")
    
    print("\n To upload documents:")
    print("   1. Copy your PDF files to the 'data' folder")
    print("   2. The folder is located at:", data_dir.absolute())
    print("   3. Then select option 1 again to process them")
    
    input("\nPress Enter to continue...")

def process_documents():
    """Process documents in the data directory."""
    print("\n" + "=" * 70)
    print("  PROCESSING DOCUMENTS")
    print("=" * 70)
    
    try:
        from qa_pipeline import RAGPipeline
        
        print("\n Initializing RAG pipeline...")
        rag = RAGPipeline()
        
        print(" Processing documents (this may take a few minutes)...")
        print("   - Extracting text from PDFs...")
        print("   - Chunking documents...")
        print("   - Generating embeddings...")
        print("   - Storing in vector database...")
        
        rag.process_documents("data", force_rebuild=False)
        
        if rag.vector_db_loaded:
            print("\n Documents processed successfully!")
            print("   You can now ask questions about your documents.")
        else:
            print("\n  No documents were processed.")
            print("   Please add PDF files to the 'data' directory first.")
    
    except Exception as e:
        print(f"\n Error processing documents: {str(e)}")
        print("\nMake sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
    
    input("\nPress Enter to continue...")

def ask_question():
    """Interactive question answering."""
    print("\n" + "=" * 70)
    print("  ASK A QUESTION")
    print("=" * 70)
    
    try:
        from qa_pipeline import RAGPipeline
        
        print("\n Loading RAG pipeline...")
        rag = RAGPipeline()
        
        if not rag.vector_db_loaded:
            print("\n  No documents processed yet!")
            print("   Please process documents first (option 1).")
            input("\nPress Enter to continue...")
            return
        
        print(" System ready!\n")
        
        while True:
            print("-" * 70)
            question = input("Enter your question (or 'back' to return to menu): ").strip()
            
            if question.lower() in ['back', 'exit', 'quit']:
                break
            
            if not question:
                print("Please enter a question.")
                continue
            
            print("\n Processing your question...")
            print("   - Creating query embedding...")
            print("   - Searching for relevant documents...")
            print("   - Generating answer...")
            
            try:
                result = rag.ask(question, use_summarization=False)
                
                print("\n" + "=" * 70)
                print("ANSWER:")
                print("=" * 70)
                print(result["answer"])
                print("\n" + "-" * 70)
                print(f"Confidence: {result['confidence']:.1%}")
                print(f"Sources used: {result['num_sources']}")
                print("-" * 70)
                
                # Ask if user wants to see sources
                show_sources = input("\nShow source documents? (y/n): ").strip().lower()
                if show_sources == 'y':
                    print("\nSOURCE DOCUMENTS:")
                    print("-" * 70)
                    for i, source in enumerate(result["sources"][:3], 1):
                        print(f"\n{i}. {source[:200]}...")
                
            except Exception as e:
                print(f"\n Error: {str(e)}")
            
            print("\n")
    
    except Exception as e:
        print(f"\n Error: {str(e)}")
        print("\nMake sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
        input("\nPress Enter to continue...")

def view_documents():
    """View information about processed documents."""
    print("\n" + "=" * 70)
    print("  PROCESSED DOCUMENTS")
    print("=" * 70)
    
    try:
        from retrieval import load_vector_db
        import config
        
        collection = load_vector_db()
        
        if collection:
            count = collection.count()
            print(f"\n Vector database loaded")
            print(f"   Collection: {config.COLLECTION_NAME}")
            print(f"   Documents stored: {count}")
            print(f"   Location: {config.VECTOR_DB_PATH}")
        else:
            print("\n No documents processed yet.")
            print("   Please process documents first (option 1).")
    
    except Exception as e:
        print(f"\n  Could not load vector database: {str(e)}")
        print("   Documents may not be processed yet.")
    
    input("\nPress Enter to continue...")

def main():
    """Main interactive loop."""
    print_header()
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies and run again.")
        return
    
    print("\n All dependencies installed!")
    print("   Ready to use the system.")
    
    while True:
        show_menu()
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            upload_documents()
            process_documents()
        elif choice == '2':
            ask_question()
        elif choice == '3':
            view_documents()
        elif choice == '4':
            print("\n Thank you for using AI Knowledge Helper!")
            print("=" * 70)
            break
        else:
            print("\n  Invalid option. Please select 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Goodbye!")
    except Exception as e:
        print(f"\n An error occurred: {str(e)}")

