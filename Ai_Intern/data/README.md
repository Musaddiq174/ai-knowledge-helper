# Data Directory

Place your PDF files in this directory.

The system will automatically:
- Extract text from all PDF files
- Process and chunk the text
- Generate embeddings
- Store in vector database

## Supported Formats
- PDF files (.pdf)

## Example
```
data/
  ├── document1.pdf
  ├── document2.pdf
  └── research_paper.pdf
```

Note: The system processes all PDF files in this directory when you run the ingestion step.

