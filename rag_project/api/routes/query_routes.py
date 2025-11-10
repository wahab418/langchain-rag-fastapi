from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from rag_project.retrival.retriever import get_retriever
from rag_project.llm.llm_model import load_llm
from rag_project.api.schema.schema import QueryLog  # your model file
from rag_project.api.db.dbs import get_db
from rag_project.api.state import othobear
from rag_project.api.create_token import decode_jwt_token
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
router = APIRouter()

retriever = get_retriever()
llm = load_llm()

class QueryRequest(BaseModel):
    query: str
    token: str
    
@router.post("/query")
#async def query_model(request: QueryRequest, db: Session = Depends(get_db), token: str= Depends(othobear)):
    
async def query_model(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        decode_token = decode_jwt_token(request.token)
        exp = decode_token.get("exp")
        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=400, message="Session Expire. Please Login!")
        
        user_email = decode_token.get("email")
        conn = psycopg2.connect(DATABASE_URL)
        corr = conn.cursor()
        corr.execute(f"select email, user_uuid from users where email='{user_email}'")
        record = corr.fetchall()
        email, user_id = record[0]
        #sqlalchemy
        if email:
            retrieved_docs = retriever.invoke(request.query)
            
            response = llm.invoke(request.query)
            response_text = response.content if hasattr(response, "content") else str(response)


            #  Save q/r db
            log_entry = QueryLog(
                query=request.query,
                response=response_text,
                user_id = user_id
            )
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)

            # Return response to client
            return {"query": request.query, "response": str(response)}

    except Exception as e:
        print("Error in /query endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))



