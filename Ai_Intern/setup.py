"""
Setup script for AI Knowledge Helper
Run this to verify installation and create necessary directories
"""
import os
from pathlib import Path

def setup_project():
    """Create necessary directories and verify setup."""
    print("Setting up AI Knowledge Helper project...")
    
    # Create directories
    directories = ["data", "vector_db"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created/verified directory: {dir_name}/")
    
    # Check for .env file
    if not Path(".env").exists():
        print("\n⚠️  .env file not found.")
        print("   Create a .env file with your OPENAI_API_KEY (optional)")
        print("   Example: OPENAI_API_KEY=your_key_here")
    else:
        print("✅ .env file found")
    
    # Check for PDF files
    pdf_files = list(Path("data").glob("*.pdf"))
    if not pdf_files:
        print("\n⚠️  No PDF files found in data/ directory")
        print("   Please add PDF files to the data/ directory")
    else:
        print(f"✅ Found {len(pdf_files)} PDF file(s) in data/")
    
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Add PDF files to the 'data/' directory")
    print("2. (Optional) Add OPENAI_API_KEY to .env file")
    print("3. Run: python main.py (for FastAPI)")
    print("   Or: jupyter notebook (for interactive notebook)")
    print("="*60)

if __name__ == "__main__":
    setup_project()

