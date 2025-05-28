Quick Start: Currently no frontend. Follow the steps below to locally run the program, and ask questions via the FASTapi UI.

Clone & enter the repo:
git clone https://github.com/<your‑github‑user>/LawyerBot.git
cd LawyerBot

Create a virtual environment & install deps
python -m venv .venv
source .venv/bin/activate          # Windows ⇒ .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt

Add environment variables
Create a .env file at the project root:
OpenAI
OPENAI_API_KEY=sk-...

Pinecone
PINECONE_API_KEY=pc-...
PINECONE_INDEX=lawyerbot-index   

Path to your combined legal JSON knowledge base
COMBINED_DATA_PATH=/absolute/path/to/legal_data.json

Launch the API server
uvicorn app.main:app --reload

Open http://127.0.0.1:8000/docs to explore and test the POST /ask endpoint.


Acknowledgements
FastAPI
OpenAI Python SDK
Pinecone
SentenceTransformers
