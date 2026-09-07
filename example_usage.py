"""
Example usage of the RAG system programmatically
(without GUI)
"""
from rag_engine import RAGEngine


def main():
    """Example usage demonstration"""
    
    # Initialize RAG engine
    rag = RAGEngine()
    
    print("=" * 60)
    print("RAG Application - Example Usage")
    print("=" * 60)
    
    # Example 1: Add sample documents
    print("\n1. Adding sample documents...")
    
    doc1 = """
    Artificial Intelligence (AI) is the simulation of human intelligence processes 
    by machines, especially computer systems. These processes include learning, 
    reasoning, and self-correction.
    
    Types of AI:
    - Narrow AI: Designed for specific tasks
    - General AI: Can understand and learn any intellectual task
    - Super AI: Theoretical AI with human-level intelligence
    """
    
    result = rag.add_knowledge("ai_basics", doc1)
    print(f"   {result['message']}")
    
    doc2 = """
    Machine Learning is a subset of AI that enables systems to learn and improve 
    from experience without being explicitly programmed. It uses algorithms and 
    statistical models to identify patterns in data.
    
    Types of Machine Learning:
    - Supervised Learning: Learning from labeled data
    - Unsupervised Learning: Finding patterns in unlabeled data
    - Reinforcement Learning: Learning through rewards and punishments
    """
    
    result = rag.add_knowledge("ml_basics", doc2)
    print(f"   {result['message']}")
    
    doc3 = """
    Deep Learning is a subset of Machine Learning inspired by biological neural networks.
    It uses neural networks with multiple layers (deep) to learn complex patterns.
    
    Applications:
    - Image Recognition: Identifying objects in images
    - Natural Language Processing: Understanding text
    - Speech Recognition: Converting audio to text
    """
    
    result = rag.add_knowledge("deep_learning", doc3)
    print(f"   {result['message']}")
    
    # Example 2: Show statistics
    print("\n2. Knowledge Base Statistics:")
    stats = rag.get_stats()
    print(f"   Total Chunks: {stats['total_chunks']}")
    print(f"   Documents: {stats['documents']}")
    
    # Example 3: Ask questions
    print("\n3. Asking Questions:")
    
    questions = [
        "What is Artificial Intelligence?",
        "What are the types of Machine Learning?",
        "Tell me about Deep Learning applications",
        "How does supervised learning work?"
    ]
    
    for question in questions:
        print(f"\n   Q: {question}")
        result = rag.generate_answer(question)
        
        print(f"   A: {result['answer'][:200]}...")
        
        if result['sources']:
            print(f"   Sources: {len(result['sources'])} document(s) retrieved")
        
        if result['error']:
            print(f"   Error: {result['error']}")
    
    # Example 4: Remove a document
    print("\n4. Removing a document...")
    result = rag.remove_knowledge("ml_basics")
    print(f"   {result['message']}")
    
    # Example 5: Final statistics
    print("\n5. Final Statistics:")
    stats = rag.get_stats()
    print(f"   Total Chunks: {stats['total_chunks']}")
    print(f"   Documents: {stats['documents']}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
