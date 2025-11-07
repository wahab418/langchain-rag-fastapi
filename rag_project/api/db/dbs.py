from rag_project.api.db.database import SessionLocal  # your database session

#  Create a database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
print("db........")