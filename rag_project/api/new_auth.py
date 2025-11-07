from sqlalchemy import create_engine
from fastapi import FastAPI
from dotenv import load_dotenv
from .state import RegisterScheme
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.post("/register")
async def create_user(RegisterScheme):
    

    pass