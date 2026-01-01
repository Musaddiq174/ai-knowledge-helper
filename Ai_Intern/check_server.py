"""Check server status and test endpoint"""
import requests
import sys

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("  CHECKING SERVER STATUS")
print("=" * 70)

# Check if server is running
try:
    print("\n1. Checking if server is running...")
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"    Server is running!")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("    Server is NOT running!")
    print("   Please start it with: python main.py")
    sys.exit(1)
except Exception as e:
    print(f"    Error: {str(e)}")
    sys.exit(1)

# Test /ask endpoint
print("\n2. Testing /ask endpoint...")
try:
    test_question = {
        "question": "What is Artificial Intelligence?",
        "top_k": None,
        "use_summarization": False,
        "evaluate": False
    }
    
    print(f"   Sending request: {test_question['question']}")
    response = requests.post(
        f"{BASE_URL}/ask",
        json=test_question,
        timeout=30
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"    Success!")
        print(f"   Answer: {result.get('answer', 'N/A')[:100]}...")
        print(f"   Confidence: {result.get('confidence', 0):.1%}")
        print(f"   Num Sources: {result.get('num_sources', 'N/A')}")
        print(f"   Has Sources: {len(result.get('sources', []))} sources")
    else:
        print(f"    Error Response:")
        print(f"   {response.text}")
        
except Exception as e:
    print(f"    Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)

