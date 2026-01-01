"""
Helper script to add PDF files to the data directory
"""
import os
import shutil
from pathlib import Path

def show_data_directory():
    """Show the data directory location and contents."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    abs_path = data_dir.absolute()
    
    print("\n" + "=" * 70)
    print("  PDF FILES LOCATION")
    print("=" * 70)
    print(f"\n Data directory: {abs_path}")
    print(f"\n Full path: {abs_path}")
    
    # Check existing PDFs
    pdf_files = list(data_dir.glob("*.pdf"))
    pdf_files.extend(list(data_dir.glob("*.PDF")))  # Also check uppercase
    
    if pdf_files:
        print(f"\n Found {len(pdf_files)} PDF file(s):")
        for i, pdf in enumerate(pdf_files, 1):
            size_kb = pdf.stat().st_size / 1024
            print(f"   {i}. {pdf.name} ({size_kb:.1f} KB)")
    else:
        print("\n  No PDF files found yet.")
    
    print("\n" + "=" * 70)
    print("  HOW TO ADD PDF FILES")
    print("=" * 70)
    print("\nMETHOD 1: Copy files manually")
    print("-" * 70)
    print("1. Open File Explorer")
    print(f"2. Navigate to: {abs_path}")
    print("3. Copy your PDF files into this folder")
    print("4. That's it! The system will find them automatically")
    
    print("\nMETHOD 2: Copy from command line")
    print("-" * 70)
    print("Example:")
    print('  copy "C:\\Users\\YourName\\Documents\\file.pdf" data\\')
    print('  copy "C:\\path\\to\\your\\document.pdf" data\\')
    
    print("\nMETHOD 3: Drag and drop")
    print("-" * 70)
    print("1. Open the 'data' folder in File Explorer")
    print("2. Drag your PDF files from another window")
    print("3. Drop them into the 'data' folder")
    
    print("\n" + "=" * 70)
    print("  QUICK TEST")
    print("=" * 70)
    print("\nAfter adding PDF files, you can:")
    print("1. Run: python interactive_qa.py")
    print("2. Select option 1 to process documents")
    print("3. Select option 2 to ask questions")
    
    # Open the folder if on Windows
    try:
        import platform
        if platform.system() == "Windows":
            print(f"\n Tip: Opening the data folder for you...")
            os.startfile(str(abs_path))
    except:
        pass
    
    print("\n" + "=" * 70)

def copy_pdf_interactive():
    """Interactive function to help copy PDF files."""
    print("\n" + "=" * 70)
    print("  COPY PDF FILE")
    print("=" * 70)
    
    source = input("\nEnter the full path to your PDF file: ").strip().strip('"')
    
    if not source:
        print("No file path provided.")
        return
    
    source_path = Path(source)
    
    if not source_path.exists():
        print(f" File not found: {source}")
        return
    
    if not source_path.suffix.lower() == '.pdf':
        print(f"  Warning: File doesn't have .pdf extension: {source_path.suffix}")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    dest_path = data_dir / source_path.name
    
    try:
        shutil.copy2(source_path, dest_path)
        print(f"\n Successfully copied!")
        print(f"   From: {source_path}")
        print(f"   To:   {dest_path}")
        print(f"\n File size: {dest_path.stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"\n Error copying file: {str(e)}")

def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("  PDF FILE HELPER")
    print("=" * 70)
    print("\nThis script helps you add PDF files to the data directory.")
    
    while True:
        print("\n" + "-" * 70)
        print("OPTIONS:")
        print("1. Show data directory location")
        print("2. Copy a PDF file (interactive)")
        print("3. Exit")
        print("-" * 70)
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == '1':
            show_data_directory()
        elif choice == '2':
            copy_pdf_interactive()
        elif choice == '3':
            print("\n Goodbye!")
            break
        else:
            print("\n  Invalid option. Please select 1-3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Goodbye!")
    except Exception as e:
        print(f"\n An error occurred: {str(e)}")

