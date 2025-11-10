from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, VARCHAR
from rag_project.api.db.database import Base
import uuid
class QueryLog(Base):
    __tablename__ = "History"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    user_id = Column(Text, nullable=False)
print("schema........")







 
   






