import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import ast

# Load dataset
df = pd.read_csv("data/RAW_recipes.csv")

# Convert lists stored as strings
df["ingredients"] = df["ingredients"].apply(ast.literal_eval)  # Convert from string to list
df["steps"] = df["steps"].apply(ast.literal_eval)
df["tags"] = df["tags"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["nutrition"] = df["nutrition"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="recipe_db",
    user="postgres",
    password="yourpassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert data
insert_query = """
INSERT INTO recipes (id, name, contributor_id, submitted, tags, nutrition, n_steps, steps, description, ingredients, minutes) 
VALUES %s ON CONFLICT (id) DO NOTHING;
"""

execute_values(
    cur,
    insert_query,
    df[['id', 'name', 'contributor_id', 'submitted', 'tags', 'nutrition', 'n_steps', 'steps', 'description', 'ingredients', 'minutes']].values.tolist()
)

# Commit & close
conn.commit()
cur.close()
conn.close()
print("✅ Data successfully loaded into PostgreSQL!")
