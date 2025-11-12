from rag_project.api.state.state import UserWorkspace, DeleteWorkspace, UpdateWorkspace
from rag_project.api.schema.schema import Workspace
from rag_project.api.db.dbs import get_db
from rag_project.api.utils.utils import decode_jwt_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Insert, Delete, Update
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()

@router.post("/create")
async def create_workspace(data: UserWorkspace, db: Session=Depends(get_db)):
    decode_token = decode_jwt_token(data.token)
    user_id = decode_token.get("user_uuid")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = db.execute(select(Workspace).where(Workspace.name == data.name)).scalar_one_or_none()

    if not result:
        db.execute(Insert(Workspace).values(name=data.name,url=str(data.url),user_uuid=user_id))
        db.commit()
        return {"message":"Workspace Created Succesfully!"}
    else:
        return {"message":"Workspace already exists!"}

@router.post("/read_workspace")
async def read_workspace(data: DeleteWorkspace, db: Session=Depends(get_db)):
    decode_token = decode_jwt_token(data.token)
    exp_date = decode_token.get("exp")
    if datetime.utcfromtimestamp(exp_date)<datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    result = db.execute(select(Workspace).where(Workspace.name==data.name)).scalar_one_or_none()
    if result:
        return {"Name":result.name,"Url":result.url}
        
    else:
        return {"message":"Workspace not Exists."}
    
@router.post("/update_workspace")
async def update_workspace(data: UpdateWorkspace, db: Session=Depends(get_db)):
    decode_token = decode_jwt_token(data.token)
    exp_date = decode_token.get("exp")
    if datetime.utcfromtimestamp(exp_date)<datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    db.execute(Update(Workspace).where(Workspace.name==data.name).values(url=str(data.url)))
    db.commit()
    
    return {"message":"Workspace Deleted Succesfully!"}

@router.delete("/delete_workspace")
async def delete_workspace(data: DeleteWorkspace, db: Session=Depends(get_db)):
    decode_token = decode_jwt_token(data.token)
    exp_date = decode_token.get("exp")
    if datetime.utcfromtimestamp(exp_date)<datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    result = db.execute(select(Workspace).where(Workspace.name == data.name)).scalar_one_or_none()

    if result:
        db.execute(Delete(Workspace).where(Workspace.name==data.name))
        db.commit()
        return {"message":"Workspace Deleted Succesfully!"}
    else:
        return {"message":"Workspace Not exists!"}





    
    
  

