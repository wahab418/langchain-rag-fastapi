from pydantic import BaseModel
from pydantic import EmailStr, AnyUrl
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
  