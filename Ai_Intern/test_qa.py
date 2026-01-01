"""Quick test script to ask questions"""
from qa_pipeline import RAGPipeline

print("=" * 70)
print("ASKING QUESTIONS")
print("=" * 70)

rag = RAGPipeline()

# Question 1
question1 = "What is Artificial Intelligence?"
print(f"\nQuestion 1: {question1}")
print("-" * 70)
result1 = rag.ask(question1)
print(f"\nAnswer: {result1['answer']}")
print(f"\nConfidence: {result1['confidence']:.1%}")
print(f"Sources used: {result1['num_sources']}")

# Question 2
question2 = "What are the main goals of AI?"
print("\n" + "=" * 70)
print(f"\nQuestion 2: {question2}")
print("-" * 70)
result2 = rag.ask(question2)
print(f"\nAnswer: {result2['answer']}")
print(f"\nConfidence: {result2['confidence']:.1%}")
print(f"Sources used: {result2['num_sources']}")

# Question 3
question3 = "Summarize the document"
print("\n" + "=" * 70)
print(f"\nQuestion 3: {question3}")
print("-" * 70)
result3 = rag.ask(question3)
print(f"\nAnswer: {result3['answer']}")
print(f"\nConfidence: {result3['confidence']:.1%}")
print(f"Sources used: {result3.get('num_sources', 0)}")

print("\n" + "=" * 70)
print("✅ All questions answered!")
print("=" * 70)

