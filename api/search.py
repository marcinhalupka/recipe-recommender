from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import psycopg2
import json
from config import (
    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT,
    FAISS_INDEX_PATH, EMBEDDING_MODEL
)

# Initialize FastAPI app
app = FastAPI(title="Recipe Search API", version="1.0")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)
cur = conn.cursor()

# Load FAISS index (from config path)
index = faiss.read_index(FAISS_INDEX_PATH)

# Load Sentence Transformer model (from config setting)
model = SentenceTransformer(EMBEDDING_MODEL)

@app.get("/search")
def search_recipes(query: str = Query(..., title="Search Query"), top_k: int = 5):
    """Search recipes using FAISS + PostgreSQL."""
    # Convert query to embedding
    query_vector = model.encode([query])

    # Perform FAISS search
    distances, indices = index.search(query_vector, top_k)

    # Get matching recipe IDs
    recipe_ids = [int(i) for i in indices[0]]

    # Query database
    cur.execute("SELECT * FROM recipes WHERE id IN %s;", (tuple(recipe_ids),))
    results = cur.fetchall()

    # Get column names
    col_names = [desc[0] for desc in cur.description]

    # Convert to JSON
    response = [dict(zip(col_names, r)) for r in results]

    return {"query": query, "results": response}

# Run API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
