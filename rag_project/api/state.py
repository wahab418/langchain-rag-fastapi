from pydantic import BaseModel
from pydantic import EmailStr
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

class LogoutScheme(BaseModel):
    email: EmailStr ="email"

class VerifyEmailScheme(BaseModel):
    token: str