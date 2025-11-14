from pydantic import BaseModel, Field
from pydantic import EmailStr, AnyUrl
from typing import Optional, List
import uuid
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
othobear = OAuth2PasswordBearer(tokenUrl="/login")
class RegisterScheme(BaseModel):
    firstname : str ="First Name"
    lastname: str ="Last Name"
    email: EmailStr="Your Email"
    password: str="Recomended strong password"
    confirm_password: str = "Must Match with privious password"

class LoginScheme(BaseModel):
    email: EmailStr
    password: str

class VerifyPasswordScheme(BaseModel):
    email: EmailStr
    password: str
 
class UserWorkspace(BaseModel):
    name : str 
    url : AnyUrl

class DeleteWorkspace(BaseModel):
    workspace_id: UUID

class UpdateWorkspace(BaseModel):
    workspace_id: UUID
    url: AnyUrl
  
class TopicGenerationInput(BaseModel):
    industry: str
    industry_other: Optional[str] = None

    audience: List[str]

    purpose: List[str]
    purpose_other: Optional[str] = None
    num_topics: int = Field(lt=5,gt=0)
    subject: Optional[str] = None
    timestamp: str