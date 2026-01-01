"""
Data Ingestion Module
Extracts text from PDF files using PyPDF
"""
import os
from pathlib import Path
from typing import List
from pypdf import PdfReader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a single PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        logger.info(f"Successfully extracted text from {pdf_path} ({len(text)} characters)")
        return text
    
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
        return ""


def ingest_pdfs(data_dir: str = "data") -> List[str]:
    """
    Ingest all PDF files from a directory.
    
    Args:
        data_dir: Directory containing PDF files
        
    Returns:
        List of extracted text strings (one per PDF)
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.warning(f"Data directory {data_dir} does not exist. Creating it...")
        data_path.mkdir(parents=True, exist_ok=True)
        return []
    
    pdf_files = list(data_path.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {data_dir}")
        return []
    
    texts = []
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(str(pdf_file))
        if text.strip():  # Only add non-empty texts
            texts.append(text)
    
    logger.info(f"Ingested {len(texts)} PDF files from {data_dir}")
    return texts


if __name__ == "__main__":
    # Test the ingestion
    texts = ingest_pdfs("data")
    print(f"Extracted {len(texts)} documents")
    if texts:
        print(f"First document length: {len(texts[0])} characters")
        print(f"First 200 characters: {texts[0][:200]}...")

