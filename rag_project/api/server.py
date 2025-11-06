# rag_project/api/server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#from rag_project.retrival.retriever import get_retriever
#from rag_project.llm.llm_model import load_llm

app = FastAPI(title="LangChain RAG API", version="1.0")

#retriever = get_retriever()
#llm = load_llm()

class QueryRequest(BaseModel):
    query: str

# Health endpoint


@app.get("/health")
async def health_check():
    return {"status": "API is running", "version": "1.0"}

# Query endpoint
@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        user_query = request.query
        
        docs = retriever.invoke(input=user_query)
        
        context = "\n".join([d.page_content for d in docs])
        
        prompt = f"Answer the question based only on the context below:\n{context}\nQuestion: {user_query}"
        
        response = llm.invoke(prompt)
        
        return {
            "query": user_query,
            "answer": response.content,
            "context_sources": [d.metadata.get("source", "unknown") for d in docs]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




