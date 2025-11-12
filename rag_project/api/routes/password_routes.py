from rag_project.api.db.dbs import get_db
from rag_project.api.schema.schema import Users
from rag_project.api.utils.utils import verify_password
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi import HTTPException
from sqlalchemy import select, Update
from rag_project.api.state.state import VerifyPasswordScheme
from sqlalchemy.orm import Session
router = APIRouter()

@router.post("/verify_password")
async def password_verification(data: VerifyPasswordScheme, db: Session= Depends(get_db)):
    user_email = data.email
    user_password = data.password
    user_db = db.execute(select(Users).where(Users.email==user_email)).scalar_one_or_none()
    if not user_db:
        raise HTTPException(status_code=400, detail="User Not Exists!")

    response = verify_password(user_password,user_db.password)

    if not response:
        raise HTTPException(status_code=400, detail="password must match!")
    
    return {"message":"Password Verify Succesfully!"}

@router.post("/forget_password")
async def forget_password(data: VerifyPasswordScheme, db: Session= Depends(get_db)):
    user_email = data.email
    db_data = db.execute(select(Users).where(Users.email==user_email)).scalar_one_or_none()
    if not db_data:
        raise HTTPException(status_code=400, detail="User Not Exists!")

    result = db.execute(Update(Users).where(Users.email==data.email).values(password=data.password))
    db.commit()
    if result:
        return {"message":"Successfku Update!"}
    else:
        return {"message":"Not Updated!"}

        
@router.post("/change_password")
async def change_password(data: VerifyPasswordScheme, db: Session= Depends(get_db)):
    user_email = data.email
    db_data = db.execute(select(Users).where(Users.email==user_email)).scalar_one_or_none()
    if not db_data:
        raise HTTPException(status_code=400, detail="User Not Exists!")

    result = db.execute(Update(Users).where(Users.email==data.email).values(password=data.password))
    db.commit()
    if result:
        return {"message":"Successfku Update!"}
    else:
        return {"message":"Not Updated!"}


