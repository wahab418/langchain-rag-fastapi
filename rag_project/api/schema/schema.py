from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, VARCHAR
from rag_project.api.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
class QueryLog(Base):
    __tablename__ = "History"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_uuid",ondelete="CASCADE"),nullable=False)
    user_relation = relationship("Users",back_populates="user_history")
print("schema........")


class Users(Base):
    __tablename__ = "users"

    user_uuid = Column(PG_UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    firstname = Column(VARCHAR, nullable=False)
    lastname = Column(VARCHAR)
    email = Column(VARCHAR, nullable=False, unique=True )
    password = Column(VARCHAR, nullable=False)

    user_history = relationship("QueryLog", back_populates="user_relation",cascade="all, delete-orphan",  passive_deletes=True)
    workspace_relation = relationship("Workspace",back_populates="workspace_relation",cascade="all, delete-orphan", passive_deletes=True)

class Workspace(Base):
    __tablename__ = "workspace"

    workspace_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    name = Column(VARCHAR, nullable=False, unique=True)
    url = Column(VARCHAR, nullable=False)
    user_uuid = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_uuid", ondelete="CASCADE"),nullable=False)

    workspace_relation = relationship("Users",back_populates="workspace_relation")
