from rag_project.api.db.database import Base, engine
from rag_project.api.routes import query_routes, user_routes, password_routes, workspace_routes
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)
print(" Database connected and tables created!")

app = FastAPI(title="LangChain RAG API", version="1.0")

@app.get("/test")
async def test_router():
    return { "message":"router is working successfully"}

app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(password_routes.router, prefix="/password", tags=["Verification"])
app.include_router(workspace_routes.router, prefix="/workspace", tags=["Workspace"])
app.include_router(query_routes.router, prefix="/query", tags=["Query"])
