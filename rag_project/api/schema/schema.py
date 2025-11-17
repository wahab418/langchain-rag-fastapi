from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, VARCHAR, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.sql import func
# from sqlalchemy.dialects.postgresql import JSONB
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
    user_topic_relation = relationship("TopicGeneration",back_populates="topic_user_relation",cascade="all, delete-orphan",passive_deletes=True)
    

class Workspace(Base):
    __tablename__ = "workspace"

    workspace_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    name = Column(VARCHAR, nullable=False)
    url = Column(VARCHAR, nullable=False)
    user_uuid = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_uuid", ondelete="CASCADE"),nullable=False)

    workspace_relation = relationship("Users",back_populates="workspace_relation")
    workspace_topic_relation = relationship("TopicGeneration",back_populates="topic_workspace_relation", cascade="all, delete-orphan",passive_deletes=True)


class TopicGeneration(Base):
    __tablename__ = "topic_generation"
    topic_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4(), nullable = False)
    
    workspace_id = Column(PG_UUID(as_uuid=True), ForeignKey("workspace.workspace_id", ondelete="CASCADE"), nullable=False)
    #############################

    generated_by_user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_uuid", ondelete="CASCADE"), nullable=True)
    generated_by_first_name = Column(String, nullable=True)
    generated_by_last_name = Column(String, nullable=True)
    title = Column(String, nullable=False)
    angle = Column(String, nullable=False)
    description = Column(String, nullable=False)  # New field
    channel_fit = Column(ARRAY(String), nullable=False)
    audience_fit = Column(ARRAY(String), nullable=False)
    why_it_works = Column(String, nullable=True)
    scores = Column(JSONB, nullable=False)
    tags = Column(ARRAY(String), nullable=True)

    # suggested_defaults = Column(JSONB, nullable=False)  # New fieldm
    # goal_alignment = Column(JSONB, nullable=False)  # New field
    # content_guidance = Column(JSONB, nullable=False)  # New field
    # audience_insights = Column(JSONB, nullable=False)  # New field
    # internal_research_config = Column(JSONB, nullable=False)  # New field
    # approved = Column(Boolean, nullable=True, server_default="false")
    # approved_at = Column(DateTime(timezone=True), nullable=True)  # When topic was approved
    # user_settings = Column(JSONB, nullable=False)  # New field

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Generated date
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=True)

    topic_user_relation = relationship("Users", back_populates="user_topic_relation")
    topic_workspace_relation = relationship("Workspace",back_populates="workspace_topic_relation")