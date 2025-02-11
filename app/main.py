import os
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from transformers import pipeline
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pineconeDB import index

# Load environment variables, Initialize OpenAI and FastAPI app
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
app = FastAPI()

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# API Request Validation
class DocumentInput(BaseModel):
    text: str
class QuestionInput(BaseModel):
    question: str

# Load JSON file
def load_json(file):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Define file path temporarily here while I build the rest of the code
file_path = "public\combinedData.json"  # Combined Json on team drive
legal_data = load_json(file_path)





# Extract text (Does Nothing)
def extract_text(data, parent_key=""):
    """ Extract text from a document """
    text = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            text.extend(extract_text(value, new_key))
# Left off here. Need Dynamic Key Extraction to extract text from legal_data if its a list/str/dict. Recursive was cool  
# def chunking is fine. 
# def pc storage needs to be better for duplicates 
# everything needs to be async. 


    return text  # Replace later








# Chunk text
def chunk_text(text):
    """ Splits extracted text into smaller overlapping chunks """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    return text_splitter.split_text(text)

# Store embeddings in Pinecone
def store_in_pinecone(chunks):
    """ Converts text chunks into embeddings and stores them in Pinecone """

    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        index.upsert(vectors=[{"id": f"chunk-{i}", "values": embedding, "metadata": {"text": chunk}}])

    return {"message": f"Stored {len(chunks)} chunks in Pinecone."}

# API to process and store documents
@app.post("/process-document")
def process_document(document: DocumentInput):
    """ Extracts text, chunks it, and stores embeddings in Pinecone """
    try:
        extracted_text = extract_text(document.text)
        chunks = chunk_text(extracted_text)
        response = store_in_pinecone(chunks)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retrieve relevant chunks
def retrieve_relevant_chunks(question, top_k=3):
    """ Searches Pinecone for the most relevant text chunks """
    question_embedding = embedding_model.encode(question).tolist()

    # Vector Search
    results = index.query(
        vector=question_embedding,
        top_k=top_k,
        include_metadata=True
    )

    retrieved_chunks = [match["metadata"]["text"] for match in results.get("matches", []) if "metadata" in match]
    
    # If no matches, return a default message
    if not retrieved_chunks:
        retrieved_chunks = ["Sorry! Not today!"]
    
    return retrieved_chunks

def generate_answer(question):
    """ Sends retrieved chunks + user question to gpt-4o-mini to generate an answer """
    relevant_chunks = retrieve_relevant_chunks(question)

    prompt = f"""
    You are an AI assistant. Use the following context to answer the question.

    Context:
    {chr(10).join(relevant_chunks)}

    Question: {question}
    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# API to handle user queries
@app.post("/ask")
def ask_question(request: QuestionInput):
    """ Retrieves relevant chunks and generates an answer """
    try:
        answer = generate_answer(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  