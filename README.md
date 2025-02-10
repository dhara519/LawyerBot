Use Docker to start project: "docker compose up"
OR
Manually install Dependencies: "pip install -r requirements.txt" or view dependencies with "pip freeze" or "pip list"

Pinecone searches for the best-matching legal text.
1: If Pinecone finds something, GPT-4o uses it to generate an answer.
2: If Pinecone finds nothing, it falls back to JSON-based retrieval.
