import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pineconeDB import index

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load JSON file
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        print("JSON file loaded successfully.")    
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


# Recursively extract text from a document
def extract_text(data, parent_key=""):
    """ Extract text from a document """
    try:    
        text = []
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}.{key}" if parent_key else key # How we keep track of the parent key as we transverse.
                text.extend(extract_text(value, new_key))
        elif isinstance(data,list):
            for i in data:
                text.extend(extract_text(i, parent_key))
        elif isinstance(data, (str, int, float, bool)):
            text.append(str(data))

        if not text:
            raise ValueError("No text extracted from the document.")
        
        return text  # Returns a list of strings
    except Exception as e:
        print(f"Error extracting text: {e}")
        raise


# Chunk text
def chunk_text(text:list):
    """ Splits extracted text into smaller overlapping chunks """
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100) # Only accepts strings
        combined_text = ",".join(text) # Joins into a single string
        return text_splitter.split_text(combined_text) # Returns a list of strings
    except Exception as e:
        print(f"Error chunking text: {e}")
        raise


# Store embeddings in Pinecone
def store_in_pinecone(chunks):
    """ Converts text chunks into embeddings and stores them in Pinecone """
    if not chunks:
        raise ValueError("No chunks provided to store in Pinecone.")
    try: 
        for i, chunk in enumerate(chunks):
            embedding = embedding_model.encode(chunk).tolist() # Convert chunk to embedding

            # Check for similarity to prevent duplicates in db: Slow af & all chunks were skipped (all had scores of .99 or 1 lol) 
            # similarity_check = index.query(vector=embedding, top_k=1, include_values=False)
            # if similarity_check and similarity_check.get("matches"):
            #     similarity_score = similarity_check["matches"][0]["score"]
            #     if similarity_score >= 0.97:  # Adjust threshold later
            #         print(f"Skipping duplicate chunk-{i} (Similarity Score: {similarity_score})")
            #         continue
                      
            index.upsert(vectors=[{"id": f"chunk-{i}", "values": embedding, "metadata": {"text": chunk}}]) 
            print(f"Stored chunk-{i} in Pinecone")
        return {"message": f"Stored {len(chunks)} chunks in Pinecone."}
    except Exception as e:
        print(f"Error storing chunks in Pinecone: {e}")
        raise

# Process document: Extract, Chunk, Store
def process_document(legal_data):
    """ Extracts text from a document and stores it in Pinecone """
    try: 
        if not legal_data:
            raise ValueError("No legal data found to process.")

        extracted_text = extract_text(legal_data)
        print("Text extracted successfully.")

        chunks = chunk_text(extracted_text)
        print("Text chunked successfully.")

        response = store_in_pinecone(chunks) # Print response for # of chunks stored
        print("Text stored in Pinecone successfully.") 

        return response
    except Exception as e:
        print(f"Error processing document:{e}")
        return {"message": "An error occurred while processing legal data for Pinecone."}
    

# Vaildate file path    
file_path = os.getenv("COMBINED_DATA_PATH")  # Combined Json on team drive
if file_path:
    file_path = os.path.normpath(file_path)
    legal_data = load_json(file_path)


# Start processing legal data
if legal_data:
        process_document(legal_data)
else: 
    print("No valid legal data loaded.")


__all__ = [ "extract_text", "chunk_text", "store_in_pinecone"]





# Extract key sections
# legal_framework = legal_data["ma_parking_system_part1"]["legal_framework"]
# appeal_process = legal_data["ma_parking_system_part1"]["appeal_process"]

# # Print example keys
# print("Legal Framework Keys:", legal_framework.keys())
# print("Appeal Process Keys:", appeal_process.keys())