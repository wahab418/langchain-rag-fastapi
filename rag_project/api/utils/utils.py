from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import Header, status
import os
import bcrypt
load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")

SECRET_KEY = os.getenv("SECRET_KEY")
import jwt
from datetime import datetime, timedelta

def create_jwt_token(data):
    expire = datetime.utcnow()+ timedelta(hours=1)
    data.update({"exp":expire})
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token

def decode_jwt_token(data):
    decode_jwt = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
    exp_date = decode_jwt.get("exp")
    if exp_date and datetime.utcfromtimestamp(exp_date) < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )

    return decode_jwt


def verify_password(user_pass, hash_pass):
    data = bcrypt.checkpw(user_pass.encode("utf-8"),hash_pass.encode("utf-8"))
    return data
    

def text_splitter(document):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    splited_docs = text_splitter.split_documents(document)
    return splited_docs




def get_current_user(Authorization: str = Header(...)):
    """
    Extracts and verifies JWT token from the Authorization header.
    Example header: Authorization: Bearer <your_token>
    """
    try:
        # Handle 'Bearer <token>' or just '<token>'
        token = Authorization.split(" ")[1] if " " in Authorization else Authorization
        decoded = decode_jwt_token(token)
        return decoded  # e.g. {"email": ..., "name": ..., "user_uuid": ...}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
