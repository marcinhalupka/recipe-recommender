CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    contributor_id INT,
    submitted DATE,
    tags TEXT[],
    nutrition NUMERIC[],
    n_steps INT,
    steps TEXT[],
    description TEXT,
    ingredients TEXT[],
    minutes INT
);
