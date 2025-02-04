from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# PostgreSQL Settings
POSTGRES_DB = os.getenv("POSTGRES_DB", "recipe_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# FAISS Index Settings
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "../retriever/recipe_search.index")

# Model Settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "../models/MiniLM_model")
