# Quick Start Guide

## Installation (5 minutes)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup**:
   ```bash
   python setup.py
   ```

3. **Add PDF files**:
   - Place your PDF files in the `data/` directory

4. **Optional: Add OpenAI API key**:
   - Create `.env` file
   - Add: `OPENAI_API_KEY=your_key_here`
   - (System works without it, using fallback)

## Usage Options

### Option 1: Jupyter Notebook (Recommended for Learning)
```bash
jupyter notebook
# Open notebook.ipynb and run cells step-by-step
```

### Option 2: Python Script
```bash
python example_usage.py
```

### Option 3: FastAPI Server
```bash
# Terminal 1: Start server
python main.py

# Terminal 2: Test API
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

### Option 4: Interactive Python
```python
from qa_pipeline import RAGPipeline

rag = RAGPipeline()
rag.process_documents("data")  # First time only
result = rag.ask("Your question here")
print(result["answer"])
```

## Project Structure

```
Ai_Intern/
├── README.md              # Main documentation
├── requirements.txt       # Dependencies
├── config.py             # Configuration
├── main.py               # FastAPI server
├── notebook.ipynb        # Step-by-step notebook
├── example_usage.py      # Example script
│
├── data_ingestion.py      # PDF extraction
├── preprocessing.py      # Text cleaning & chunking
├── embeddings.py         # Embedding generation
├── retrieval.py          # Vector search
├── qa_pipeline.py        # RAG pipeline
├── evaluation.py         # Quality metrics
├── ml_components.py      # Summarization, classification
│
├── data/                 # Put PDFs here
└── vector_db/           # Auto-created
```

## Common Commands

```bash
# Process documents
python -c "from qa_pipeline import RAGPipeline; RAGPipeline().process_documents('data')"

# Start API server
python main.py

# Run example
python example_usage.py

# Check health
curl http://localhost:8000/health
```

## Troubleshooting

**Issue**: "No module named 'X'"
- **Fix**: `pip install -r requirements.txt`

**Issue**: "No PDF files found"
- **Fix**: Add PDF files to `data/` directory

**Issue**: "Vector database not found"
- **Fix**: Run `rag.process_documents("data")` first

**Issue**: "OpenAI API error"
- **Fix**: Check `.env` file or use without API key (fallback mode)

## Next Steps

1. Add your PDF documents to `data/`
2. Run the notebook or example script
3. Experiment with different questions
4. Try different chunk sizes in `config.py`
5. Explore evaluation metrics
6. Customize prompts and parameters

## Support

- Check `README.md` for detailed documentation
- See `PROJECT_SUMMARY.md` for design decisions
- Review `notebook.ipynb` for step-by-step guide

