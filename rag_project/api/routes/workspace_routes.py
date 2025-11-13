from rag_project.api.state.state import UserWorkspace, DeleteWorkspace, UpdateWorkspace
from rag_project.api.schema.schema import Workspace
from rag_project.api.db.dbs import get_db
from rag_project.api.utils.utils import decode_jwt_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Insert, Delete, Update
from sqlalchemy.orm import Session
from datetime import datetime
from rag_project.api.db.vector_db import store_vector_db, delete_vector_db
from rag_project.api.scrape.scrape import web_scraper
router = APIRouter()

@router.post("/create_workspace")
async def create_workspace(data: UserWorkspace, db: Session=Depends(get_db)):
    decode_token = decode_jwt_token(data.token)
    user_id = decode_token.get("user_uuid")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = db.execute(select(Workspace).where(Workspace.name == data.name)).scalar_one_or_none()

    if result:
        return {"message": "Workspace already exists!"}

    # Step 1: Create new workspace
    new_workspace = Workspace(name=data.name, url=str(data.url), user_uuid=user_id)
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)  # ensures we have new_workspace.workspace_id

    # Step 2: Scrape and store data
    docs = web_scraper(str(data.url))
    store_vector_db(docs, new_workspace.workspace_id)

    return {"message": "Workspace Created Successfully!"}

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
        workspace_id = result.workspace_id
        db.delete(result)
        db.commit()

        delete_vector_db(workspace_id)
        return {"message":"Workspace Deleted Succesfully!"}
    else:
        return {"message":"Workspace Not exists!"}





    
    
  

