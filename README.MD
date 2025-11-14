# LangChain RAG System with FastAPI and Neon PostgreSQL

A Retrieval-Augmented Generation (RAG) system built using LangChain, FastAPI, and PostgreSQL (Neon Cloud DB).This project enables users to query information from a document-based knowledge base using an integrated LLM (Groq or OpenAI).

=> Project Description:

   The system performs the following steps:

1. Loads and splits PDF data
2. Creates embeddings and stores them in a Chroma vector database
3. Uses a language model (LLM) to generate intelligent responses
4. Stores all user queries and LLM responses in a Neon PostgreSQL database

=> Folder Structure

rag_project/
├── api/
│ └── server.py # FastAPI server file (main API)
│
├── db/
│ ├── database.py # Database connection setup
│ ├── dbs.py # Session dependency for FastAPI
│
├── schema/
│ └── schema.py # SQLAlchemy model (QueryLog)
│
├── loaders/
│ └── pdf_loader.py # PDF loader
│
├── utils/
│ └── text_splitter.py # Document text splitter
│
├── embeddings/
│ └── embed_store.py # Vector store creation/loading
│
├── retrival/
│ └── retriever.py # Document retriever
│
├── llm/
│ └── llm_model.py # LLM model loading (Groq, OpenAI, etc.)
│
├── data/
│ └── raw/ # Folder containing PDFs
│
└── main.py # Pipeline to process documents and create embeddings

    ## Environment:

1. create a virtual envirnment:
     python -m venv .venv
  
2. Now activate the virtual envirnment:
    .venv\Scripts\activate

3. Install all Dependencies:
    pip install -r requirements.txt

4. Create a .env file in the project root:
    DATABASE_URL=postgresql+psycopg2://<your_user>:<your_password>@<your_neon_host>/<your_db>?sslmode=require

5. Run the App(Start the FastAPI server):
    uvicorn rag_project.api.server:app --reload

    => Features:

    -> Document ingestion from PDFs
    -> Text splitting for embedding
    -> Vectorstore creation using Chroma
    -> Retrieval with similarity search
    -> LLM response generation
    -> User query and response logging into Neon PostgreSQL
    -> REST API via FastAPI

    ## Technologies Used

   -> LangChain
   -> FastAPI
   -> PostgreSQL (Neon)
   -> SQLAlchemy
   -> Pydantic
   -> dotenv
   -> Chroma Vector Store
   -> HuggingFaceEmbeddings
   -> Groq / OpenAI Model


    ## Testing the API


uvicorn rag_project.api.server:app --reload

{
    "message": "Successfull login.",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsaUBnbWFpbC5jb20iLCJuYW1lIjoiYWxpIiwidXNlcl91dWlkIjoiNjkzODNkY2YtODkxNS00ZTE1LTliMDQtNGEyZDhkYTAxNjhlIiwiZXhwIjoxNzYzMTE4OTA5fQ.2tre7TcLQ7xAuSBQPJYyp5K7VTx68qoiyTFPVjnpts8",
    "token_type": "Bearer"
}

{
    "message": "Workspace Created Successfully!",
    "workspace_id": "4d0a2cf5-94a1-4bf8-81b7-5fb9a85ae482",
    "name": "revnix",
    "url": "https://revnix.com/",
    "user_uuid": "69383dcf-8915-4e15-9b04-4a2d8da0168e"
}


https://revnix.com/

{
  "firstname": "ali",
  "lastname": "khan",
  "email": "ali@gmail.com",
  "password": "123",
  "confirm_password": "123"
}
{
  "email": "ali@gmail.com",
  "password": "123"
}


rag_project.api.scrape.scrape.py


create a workspace for each user
each workspace has id,name, url
crud
use the url and scrape data using crawl4ai and build a vectoe store.

crud
scrape url content
vector db


create topic generation routes.
get pyload from forntend
based on the user topic, generate topic and store it inside topic generation routes.

http://127.0.0.1:8000/topic_generation/generate_topic

{
  "industry": "AI",
  "audience": ["Developers"],
  "purpose": ["Research"],
  "num_topics": 2,
  "timestamp": "2025-11-14T11:00:00Z"
}