# How to Use AI Knowledge Helper - Step-by-Step Guide

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages (may take a few minutes).

### Step 2: Add Your PDF Documents

**Option A: Using File Explorer**
1. Open the `data` folder in your project directory
2. Copy your PDF files into this folder
3. That's it! The system will find them automatically

**Option B: Using Command Line**
```bash
# Copy PDF files to data directory
copy "C:\path\to\your\file.pdf" data\
```

### Step 3: Run the Interactive Script
```bash
python interactive_qa.py
```

Then follow the menu:
1. Select option **1** to process your documents
2. Select option **2** to ask questions
3. Type your question and get answers!

---

## Detailed Usage Guide

### Method 1: Interactive Script (Easiest) 

**Run:**
```bash
python interactive_qa.py
```

**Features:**
- Simple menu interface
- Step-by-step guidance
- Automatic document processing
- Interactive Q&A

**Menu Options:**
1. **Upload/Process PDF documents** - Process PDFs in the data folder
2. **Ask a question** - Query your documents
3. **View processed documents** - Check what's loaded
4. **Exit** - Close the program

---

### Method 2: Jupyter Notebook (For Learning)

**Run:**
```bash
jupyter notebook
```

**Then:**
1. Open `notebook.ipynb`
2. Run cells step-by-step
3. See each component in action

**Best for:**
- Understanding how RAG works
- Experimenting with parameters
- Learning the pipeline

---

### Method 3: FastAPI Server (For API Access)

**Start Server:**
```bash
python main.py
```

**Query via API:**
```bash
# Using curl
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is the main topic?\"}"

# Using Python
import requests
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is the main topic?"}
)
print(response.json())
```

**API Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /ask` - Ask a question
- `POST /process` - Process documents

---

### Method 4: Python Script (Programmatic)

**Example:**
```python
from qa_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline()

# Process documents (first time only)
rag.process_documents("data")

# Ask questions
result = rag.ask("What is the main topic?")
print(result["answer"])
print(f"Confidence: {result['confidence']}")
```

---

## Example Workflow

### 1. Prepare Your Documents
```
data/
  ├── research_paper.pdf
  ├── company_report.pdf
  └── technical_doc.pdf
```

### 2. Process Documents
```bash
python interactive_qa.py
# Select option 1
```

**Output:**
```
 Processing documents...
   - Extracting text from PDFs...
   - Chunking documents...
   - Generating embeddings...
   - Storing in vector database...
 Documents processed successfully!
```

### 3. Ask Questions
```bash
# In interactive_qa.py, select option 2
```

**Example Questions:**
- "What is the main topic of the document?"
- "Summarize the key points"
- "What are the important findings?"
- "Explain the methodology used"
- "What are the conclusions?"

**Example Output:**
```
ANSWER:
======================================================================
The main topic is artificial intelligence and machine learning.
The document discusses various applications including natural language
processing, computer vision, and autonomous systems. Key findings
include...

----------------------------------------------------------------------
Confidence: 85.3%
Sources used: 3
----------------------------------------------------------------------
```

---

## Troubleshooting

### Problem: "No module named 'X'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "No PDF files found"
**Solution:**
- Make sure PDF files are in the `data/` folder
- Check file extensions are `.pdf` (not `.PDF`)
- Verify files are not corrupted

### Problem: "Vector database not found"
**Solution:**
- Run document processing first (option 1 in interactive script)
- Or run: `python -c "from qa_pipeline import RAGPipeline; RAGPipeline().process_documents('data')"`

### Problem: "OpenAI API error"
**Solution:**
- System works without OpenAI API (uses fallback)
- For better answers, add API key to `.env` file:
  ```
  OPENAI_API_KEY=your_key_here
  ```

### Problem: Processing is slow
**Solution:**
- This is normal for first-time processing
- Embedding generation takes time
- Subsequent queries are fast

---

## Tips for Best Results

1. **Document Quality:**
   - Use text-based PDFs (not scanned images)
   - Ensure PDFs are not password-protected
   - Larger documents = better coverage

2. **Question Format:**
   - Ask specific questions
   - Use natural language
   - Be clear about what you want

3. **Multiple Documents:**
   - System searches across all documents
   - Questions can reference any document
   - Answers combine information from multiple sources

4. **Re-processing:**
   - If you add new PDFs, process again
   - Use `force_rebuild=True` to rebuild from scratch

---

## File Structure

```
Ai_Intern/
├── data/                  ← Put your PDFs here
│   ├── document1.pdf
│   └── document2.pdf
├── vector_db/             ← Auto-created (stores embeddings)
├── interactive_qa.py      ← Easiest way to use
├── notebook.ipynb          ← Step-by-step learning
├── main.py                ← FastAPI server
└── example_usage.py       ← Simple example script
```

---

## Need Help?

1. Check `README.md` for detailed documentation
2. See `QUICK_START.md` for quick reference
3. Review `PROJECT_SUMMARY.md` for design details
4. Run `python setup.py` to verify installation

---

## Example Session

```bash
$ python interactive_qa.py

======================================================================
  AI KNOWLEDGE HELPER - Interactive Q&A System
======================================================================

 All dependencies installed!

----------------------------------------------------------------------
MAIN MENU
----------------------------------------------------------------------
1. Upload/Process PDF documents
2. Ask a question
3. View processed documents
4. Exit
----------------------------------------------------------------------
Select an option (1-4): 1

======================================================================
  PROCESSING DOCUMENTS
======================================================================

 Processing documents...
 Documents processed successfully!

Select an option (1-4): 2

Enter your question: What is artificial intelligence?

 Processing your question...
======================================================================
ANSWER:
======================================================================
Artificial intelligence is a branch of computer science that aims to
create systems capable of performing tasks requiring human intelligence...

Confidence: 82.3%
Sources used: 3
```

---

**That's it! You're ready to use the system.** 🚀

