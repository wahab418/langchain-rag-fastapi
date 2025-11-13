from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from rag_project.retrival.retriever import get_retriever
from rag_project.llm.llm_model import load_llm
from rag_project.api.schema.schema import QueryLog, Users 
from rag_project.api.db.dbs import get_db
from rag_project.api.state.state import othobear, RegisterScheme, LoginScheme
from rag_project.api.utils.utils import decode_jwt_token, get_current_user, create_jwt_token
from sqlalchemy import select, delete
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
router = APIRouter()
import bcrypt

@router.post("/register")
async def register(user: RegisterScheme,db:Session=Depends(get_db)):
    existing_record =  db.execute(select(Users).where(Users.email == user.email)).scalar_one_or_none()
    if existing_record:
        raise HTTPException(status_code=400, detail="User Already exists")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passord must match with confirm password")
    hash_pass = bcrypt.hashpw(user.password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
    new_user = Users(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hash_pass
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return {"message":"Succesfully register"}


@router.post("/login")
async def login(user_request: LoginScheme, db:Session=Depends(get_db)):
    existing_record =  db.execute(select(Users).where(Users.email == user_request.email)).scalar_one_or_none()
    if not existing_record:
        raise HTTPException(status_code=400, detail="Please Register Yourself before Login")

    original_password =  existing_record.password

    response = bcrypt.checkpw(
        user_request.password.encode("utf-8"),
        original_password.encode("utf-8")
    )
    if not response:
        raise HTTPException(status_code=400, detail="password must match!")
    
    token = create_jwt_token({"email":user_request.email,"name":existing_record.firstname,"user_uuid":str(existing_record.user_uuid)})
    return {"message": "Successfull login.","access_token":token,"token_type":"Bearer"}

@router.post("/verify_email")
async def email_verification(data=Depends(get_current_user), db:Session = Depends(get_db)):
    email_token = data.get("email")

    if not email_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    # conn = psycopg2.connect(DATABASE_URL)
    # corr = conn.cursor()
    email_db = db.execute(select(Users).where(email_token == Users.email)).scalar_one_or_none()

    # corr.execute(f"select * from users where email='{email_token}'")
    # email_db = corr.fetchone()

    if not email_db:
        raise HTTPException(status_code=400,detail="User not exist.")
    
    return {"message":"Email verified"}



@router.post("/resend_verification")
async def resend_email_verification(data=Depends(get_current_user), db:Session = Depends(get_db)):
    email_token = data.get("email")

    if not email_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    # conn = psycopg2.connect(DATABASE_URL)
    # corr = conn.cursor()
    email_db = db.execute(select(Users).where(email_token == Users.email)).scalar_one_or_none()

    # corr.execute(f"select * from users where email='{email_token}'")
    # email_db = corr.fetchone()

    if not email_db:
        raise HTTPException(status_code=400,detail="User not exist.")
    
    return {"message":"Email verified Again!"}


@router.delete("/logout")
async def logout(data = Depends(get_current_user), db: Session = Depends(get_db)):
    user_email = data.get("email")

    email_db = db.execute(select(Users).where(Users.email == user_email)).scalar_one_or_none()


    if not email_db:
        raise HTTPException(status_code=400,detail="User not exist.")
        

    result = db.execute(delete(Users).where(Users.email == user_email))
    db.commit()
    if result.rowcount > 0:
        return {"message":"Successfully Deleted!"}

    else:
        return {"message":"User Not  Deleted!"}



    
