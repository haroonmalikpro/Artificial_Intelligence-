"""
Configuration settings for the Tkinter RAG application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# ChromaDB Configuration
CHROMA_DB_PATH = "./chroma_data"
COLLECTION_NAME = "documents"

# LLM Configuration
LLM_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Application Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3  # Number of documents to retrieve
