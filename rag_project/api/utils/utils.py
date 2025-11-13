from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

