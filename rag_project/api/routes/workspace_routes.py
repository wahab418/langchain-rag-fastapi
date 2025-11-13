from rag_project.api.state.state import UserWorkspace, DeleteWorkspace, UpdateWorkspace
from rag_project.api.schema.schema import Workspace
from rag_project.api.db.dbs import get_db
from rag_project.api.utils.utils import decode_jwt_token, get_current_user
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select, Insert, Delete, Update
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from rag_project.api.db.vector_db import store_vector_db, delete_vector_db
from rag_project.api.scrape.scrape import web_scraper
router = APIRouter()

@router.post("/create_workspace")
async def create_workspace(data: UserWorkspace, decode_token = Depends(get_current_user), db: Session=Depends(get_db), background_tasks: BackgroundTasks = None):
    user_id = decode_token.get("user_uuid")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    '''
    result = db.execute(select(Workspace).where(Workspace.name == data.name)).scalar_one_or_none()

    if result:
        return {"message": "Workspace already exists!"}
    '''
    # Step 1: Create new workspace
    new_workspace = Workspace(name=data.name, url=str(data.url), user_uuid=user_id)
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)  # ensures we have new_workspace.workspace_id
    
    # Step 2: Scrape and store data
    background_tasks.add_task(store_vector_db,web_scraper(str(data.url)),new_workspace.workspace_id )
    #store_vector_db(docs, new_workspace.workspace_id)

    return {"message": "Workspace Created Successfully!",
            "workspace_id":new_workspace.workspace_id,
            "name":new_workspace.name,
            "url":new_workspace.url,
            "user_uuid":new_workspace.user_uuid}

@router.get("/read_workspace")
async def read_workspace(workspace_id: UUID, db: Session=Depends(get_db), decode_token = Depends(get_current_user)):
    exp_date = decode_token.get("exp")
    if datetime.utcfromtimestamp(exp_date)<datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    result = db.execute(select(Workspace).where(Workspace.workspace_id ==workspace_id)).scalar_one_or_none()
    if result:
        return {
            "workspace_id":result.workspace_id,
            "name":result.name,
            "url":result.url,
            "user_uuid":result.user_uuid}  
    else:
        return {"message":"Workspace not Exists."}
    
@router.put("/update_workspace")
async def update_workspace(data: UpdateWorkspace, db: Session=Depends(get_db),decode_token = Depends(get_current_user)):
    exp_date = decode_token.get("exp")
    if datetime.utcfromtimestamp(exp_date)<datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    workspace = db.execute(select(Workspace).where(Workspace.workspace_id == data.workspace_id)).scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    workspace.url = str(data.url)
    db.commit()
    db.refresh(workspace)
    
    return {
            "workspace_id":workspace.workspace_id,
            "name":workspace.name,
            "url":workspace.url,
            "user_uuid":workspace.user_uuid}

@router.delete("/delete_workspace")
async def delete_workspace(workspace_id: UUID, db: Session=Depends(get_db), decode_token = Depends(get_current_user), background_task: BackgroundTasks = None):
    exp_date = decode_token.get("exp")
    if datetime.utcfromtimestamp(exp_date)<datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    result = db.execute(select(Workspace).where(Workspace.workspace_id == workspace_id)).scalar_one_or_none()

    if result:
        workspace_id = result.workspace_id
        db.delete(result)
        db.commit()
        background_task.add_task(delete_vector_db,workspace_id)
        return {"message": "Workspace Deleted Successfully!", "workspace_id": workspace_id}
    else:
        return {"message":"Workspace Not exists!"}





    
    
  

