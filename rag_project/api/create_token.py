from dotenv import load_dotenv
from fastapi import HTTPException
import os
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



