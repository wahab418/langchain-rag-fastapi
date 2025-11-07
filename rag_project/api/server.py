# rag_project/api/server.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from rag_project.retrival.retriever import get_retriever
from rag_project.llm.llm_model import load_llm
from rag_project.api.schema.schema import QueryLog  # your model file
from rag_project.api.db.dbs import get_db
from rag_project.api.db.database import Base, engine

Base.metadata.create_all(bind=engine)
print(" Database connected and tables created!")

app = FastAPI(title="LangChain RAG API", version="1.0")

retriever = get_retriever()
llm = load_llm()

#  Request body model
class QueryRequest(BaseModel):
    query: str
    user_id: str | None = None

@app.post("/query")
async def query_model(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        retrieved_docs = retriever.invoke(request.query)
        
        response = llm.invoke(request.query)
        response_text = response.content if hasattr(response, "content") else str(response)


        #  Save q/r db
        log_entry = QueryLog(
            query=request.query,
            response=response_text
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)

        # Return response to client
        return {"query": request.query, "response": str(response)}

    except Exception as e:
        print("Error in /query endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))
