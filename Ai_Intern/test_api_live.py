"""Test FastAPI endpoints"""
import requests
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("  TESTING FASTAPI ENDPOINTS")
print("=" * 70)

# Wait for server to start
print("\nWaiting for server to start...")
time.sleep(3)

try:
    # Test 1: Health check
    print("\n1. Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 2: Root endpoint
    print("\n2. Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 3: Ask a question
    print("\n3. Testing /ask endpoint...")
    print("   Question: What is Artificial Intelligence?")
    response = requests.post(
        f"{BASE_URL}/ask",
        json={"question": "What is Artificial Intelligence?"},
        timeout=30
    )
    print(f"   Status Code: {response.status_code}")
    result = response.json()
    print(f"\n   Answer: {result['answer'][:200]}...")
    print(f"   Confidence: {result['confidence']:.1%}")
    print(f"   Sources: {result['num_sources']}")
    
    print("\n" + "=" * 70)
    print("✅ All endpoints working!")
    print("=" * 70)
    print(f"\nServer is running at: {BASE_URL}")
    print(f"Interactive docs: {BASE_URL}/docs")
    print("\nTo stop the server, press CTRL+C in the server terminal.")
    
except requests.exceptions.ConnectionError:
    print("\n❌ Error: Could not connect to server.")
    print("   Make sure the server is running: python main.py")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

