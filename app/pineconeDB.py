import os
from dotenv import load_dotenv
from pinecone import Pinecone,ServerlessSpec

# Load environment variables, Initialize Pinecone & Get pc index name
load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

# Test: Ensure index name in .env is valid 
if not index_name:
    raise ValueError("PINECONE_INDEX environment variable is invalid.")

# Test: Ensure the index exists in pc before initializing index connection
existing_indexes = [index["name"] for index in pc.list_indexes().get("indexes", [])]
if index_name not in existing_indexes:
    print(f"Existing indexes in Pinecone: {pc.list_indexes()}")
    pc.create_index(
        name=index_name,
        dimension=384,  # Match huggings embedding model
        metric="cosine",
        spec= ServerlessSpec(
            cloud= "aws",
            region= "us-east-1")
    )
else:
    # Initialize Pinecone Index Connection using index's host URL
    index_details = pc.describe_index(index_name)
    index = pc.Index(host= index_details.host)
    
__all__ = ["pc", "index", "index_name", "index_details"]