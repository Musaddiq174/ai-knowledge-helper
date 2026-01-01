# AI Knowledge Helper - RAG System

A mini Retrieval-Augmented Generation (RAG) question-answering tool that ingests PDF documents, processes them, and answers questions using semantic search and LLM reasoning.

## Features

- 📄 **PDF Document Ingestion**: Extract text from PDF files using PyPDF
- 🔧 **Text Preprocessing**: Clean and chunk documents for optimal retrieval
- 🧠 **Embeddings**: Generate semantic embeddings using SentenceTransformers
- 💾 **Vector Database**: Store and search embeddings using ChromaDB
- ❓ **Question Answering**: RAG pipeline with retrieval + LLM reasoning
- 📊 **Evaluation**: Check if retrieved text matches query intent
- 🤖 **ML Component**: Document summarization
- 🚀 **FastAPI Endpoint**: REST API for querying the system

## Project Structure

```
Ai_Intern/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.py                # Configuration settings
├── main.py                # FastAPI application entry point
├── notebook.ipynb          # Step-by-step Jupyter notebook
├── data_ingestion.py       # PDF text extraction
├── preprocessing.py        # Text cleaning and chunking
├── embeddings.py           # Embedding generation
├── retrieval.py            # Vector search and retrieval
├── qa_pipeline.py          # RAG pipeline implementation
├── evaluation.py           # Evaluation functions
├── ml_components.py        # Summarization and other ML features
├── data/                   # Directory for PDF files
│   └── sample.pdf          # Sample PDF (add your own)
└── vector_db/              # ChromaDB storage (created automatically)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key** (optional, for GPT-4o):
   - Create a `.env` file in the project root
   - Add: `OPENAI_API_KEY=your_api_key_here`
   - If not using OpenAI, the system will use a local fallback

5. **Add PDF files**:
   - Place your PDF files in the `data/` directory
   - Or use the sample PDF provided

## Usage

### Option 1: Jupyter Notebook (Recommended for Learning)

1. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

2. **Open `notebook.ipynb`** and run cells step by step

3. **Follow the workflow**:
   - Data ingestion
   - Preprocessing
   - Embedding generation
   - Vector database setup
   - Question answering
   - Evaluation

### Option 2: Python Scripts

1. **Process documents** (run once):
   ```bash
   python -c "from data_ingestion import ingest_pdfs; from preprocessing import preprocess_text; from embeddings import create_embeddings; from retrieval import setup_vector_db; import os; texts = ingest_pdfs('data'); chunks = preprocess_text(texts); embeddings, texts = create_embeddings(chunks); setup_vector_db(embeddings, texts)"
   ```

2. **Run FastAPI server**:
   ```bash
   python main.py
   ```

3. **Query the API**:
   ```bash
   curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"What is the main topic?\"}"
   ```

   Or use Python:
   ```python
   import requests
   response = requests.post("http://localhost:8000/ask", json={"question": "What is the main topic?"})
   print(response.json())
   ```

### Option 3: Interactive Python

```python
from qa_pipeline import RAGPipeline

# Initialize pipeline
rag = RAGPipeline()

# Process documents (first time only)
rag.process_documents("data/")

# Ask a question
answer = rag.ask("What is the document about?")
print(answer)
```

## API Endpoints

### POST /ask

Query the RAG system with a question.

**Request:**
```json
{
  "question": "What is the main topic of the document?"
}
```

**Response:**
```json
{
  "answer": "The main topic is...",
  "sources": ["chunk1", "chunk2"],
  "confidence": 0.85
}
```

### GET /health

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

## Configuration

Edit `config.py` to customize:

- Embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`)
- Chunk size and overlap
- Number of retrieved chunks
- LLM model (OpenAI GPT-4o or local fallback)

## Key Design Decisions

1. **SentenceTransformers over OpenAI Embeddings**: Free, no API key needed, runs locally
2. **ChromaDB over FAISS**: Easier to use, persistent storage, better for beginners
3. **Chunking Strategy**: 500 tokens with 50 token overlap for context preservation
4. **Retrieval Method**: Cosine similarity search in vector space
5. **LLM Integration**: OpenAI GPT-4o with fallback to local models

## Evaluation Metrics

The system includes evaluation functions to check:
- **Relevance Score**: How well retrieved chunks match the query
- **Coverage**: Whether all aspects of the question are addressed
- **Semantic Similarity**: Embedding-based similarity between query and retrieved text

## ML Components

### Summarization
- Automatically generates summaries of retrieved document chunks
- Helps provide concise context to the LLM

### Question Classification (Optional)
- Classifies questions by type (factual, analytical, comparative, etc.)
- Can be enabled in `ml_components.py`

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **PDF Reading Error**: Ensure PDFs are not password-protected or corrupted

3. **OpenAI API Error**: Check your API key in `.env` file, or use local embeddings

4. **ChromaDB Error**: Delete `vector_db/` folder and re-run the setup

## Future Improvements

- [ ] Support for more document types (CSV, DOCX, TXT)
- [ ] Multi-language support
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Hybrid search (keyword + semantic)
- [ ] Query expansion and re-ranking
- [ ] User feedback loop for improving retrieval
- [ ] Deployment to cloud (AWS, GCP, Azure)

## License

This project is for educational purposes.

## Author

AI/ML Intern Project - RAG System Implementation

