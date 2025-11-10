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


uvicorn rag_project.api.server:app

{
  "message": "Successfull login.",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsaS5raGFuQGdtYWlsLmNvbSIsImV4cCI6MTc2Mjc1ODU2M30.CGPj68xr_P-H6xxmPErXCV5IGJ8MfPHTt2-gxMqkRQI",
  "token_type": "Bearer"
}
