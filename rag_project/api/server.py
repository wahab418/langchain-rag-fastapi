# rag_project/api/server.py
from fastapi import FastAPI

from rag_project.api.db.database import Base, engine
from rag_project.api.routes import query_routes
from fastapi import FastAPI, Request, BackgroundTasks, Depends, HTTPException
from .state import RegisterScheme, LoginScheme, LogoutScheme, VerifyEmailScheme
import os
import psycopg2
import bcrypt
from .create_token import create_jwt_token, decode_jwt_token
from .state import othobear
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


Base.metadata.create_all(bind=engine)
print(" Database connected and tables created!")

app = FastAPI(title="LangChain RAG API", version="1.0")


@app.post("/register")
async def register(user: RegisterScheme):
    # return {"first_name":data.firstname,"last_name":data.lastname}
    conn = psycopg2.connect(DATABASE_URL)
    corr = conn.cursor()
    corr.execute(f"select * from users where email='{user.email}'")
    record = corr.fetchall()
    if record:
        raise HTTPException(status_code=400, detail="User Already exists")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passord must match with confirm password")
    hash_pass = bcrypt.hashpw(user.password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
    record = corr.execute(f"INSERT INTO users (firstname, lastname, email, password, confirm_password) VALUES ('{user.firstname}', '{user.lastname}', '{user.email}', '{hash_pass}','{hash_pass}');")
    conn.commit()
    corr.close()
    conn.close()
    return {"message":"Succesfully register"}


@app.post("/login")
async def login(user_request: LoginScheme):
    conn = psycopg2.connect(DATABASE_URL)
    corr = conn.cursor()
    corr.execute(f"select * from users where email='{user_request.email}'")
    record = corr.fetchone()
    if not record:
        raise HTTPException(status_code=400, detail="Please Register yourself before login")
    hastpass= bcrypt.hashpw(user_request.password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

    corr.execute(f"select password from users where email='{user_request.email}'")
    original_password = corr.fetchone()
    response = bcrypt.checkpw(user_request.password.encode("utf-8"), original_password[0].encode("utf-8"))
    if not response:
        raise HTTPException(status_code=400, detail="password must match!")
    
    token = create_jwt_token({"email":user_request.email})
    return {"message": "Successfull login.","access_token":token,"token_type":"Bearer"}

@app.post("/verify_email")
async def email_verification(data: VerifyEmailScheme):
    decode_token = decode_jwt_token(data.token)
    email_token = decode_token.get("email")

    if not email_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    conn = psycopg2.connect(DATABASE_URL)
    corr = conn.cursor()

    corr.execute(f"select * from users where email='{email_token}'")
    email_db = corr.fetchone()

    if not email_db:
        raise HTTPException(400,details="User not exist.")
    
    return {"message":"Email verified"}



@app.post("/resend_verification")
async def resend_email_verification(token: str):
    decode_token = decode_jwt_token(token)
    email_token = decode_token.get("email")

    if not email_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    conn = psycopg2.connect(DATABASE_URL)
    corr = conn.cursor()

    corr.execute(f"select * from users where email='{email_token}'")
    email_db = corr.fetchone()

    if not email_db:
        raise HTTPException(400,details="User not exist.")
    
    return {"message":"Email verified Again!"}


@app.delete("/logout")
async def logout(data: LogoutScheme):
    conn = psycopg2.connect(DATABASE_URL)
    corr = conn.cursor()

    corr.execute(f"select * from users where email='{data.email}'")
    email_db = corr.fetchone()

    if not email_db:
        raise HTTPException(400,details="User not exist.")
    
    corr.execute(f"DELETE from users where email='{data.email}'")
    conn.commit()
    corr.close()
    conn.close()

    return {"message":"Successfully Deleted!"}




@app.get("/test")
async def test_router():
    return { "message":"router is working successfully"}



app.include_router(query_routes.router, prefix="/query", tags=["Query"])



