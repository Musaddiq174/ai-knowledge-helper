"""Quick dependency check"""
import sys

deps = {
    'sentence_transformers': 'sentence-transformers',
    'chromadb': 'chromadb',
    'pypdf': 'pypdf',
    'numpy': 'numpy',
    'openai': 'openai'
}

print("Checking dependencies...")
print("=" * 50)

all_ok = True
for module, package in deps.items():
    try:
        __import__(module)
        print(f" {package}: OK")
    except ImportError:
        print(f" {package}: NOT INSTALLED")
        all_ok = False

print("=" * 50)
if all_ok:
    print(" All dependencies installed!")
    sys.exit(0)
else:
    print("  Missing dependencies. Install with:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

