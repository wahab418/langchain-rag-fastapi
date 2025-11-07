# rag_project/api/server.py
from fastapi import FastAPI
from rag_project.api.db.database import Base, engine
from rag_project.api.routes import query_routes


Base.metadata.create_all(bind=engine)
print(" Database connected and tables created!")

app = FastAPI(title="LangChain RAG API", version="1.0")


@app.get("/test")
async def test_router():
    return { "message":"router is working successfully"}


app.include_router(query_routes.router, prefix="/query", tags=["Query"])



