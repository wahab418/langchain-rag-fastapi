from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from rag_project.api.state.state import TopicGenerationInput
from rag_project.api.model_state.model_state import BasicTopicGenerationList
from rag_project.api.schema.schema import TopicGeneration, Workspace, Users
from rag_project.api.utils.utils import get_current_user
from rag_project.api.prompts.prompts import prompt
from rag_project.llm.llm_model import load_llm
from rag_project.api.db.dbs import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select, Delete
from uuid import UUID
router = APIRouter()

@router.post("/generate_topic")
async def generate_topic(data:TopicGenerationInput, db:Session = Depends(get_db), token= Depends(get_current_user), background_tasks: BackgroundTasks = None):
    user_id = token.get("user_uuid")
    exp_date = token.get("exp")
    if datetime.utcfromtimestamp(exp_date) <datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    workspace_db = db.execute(select(Workspace).where(Workspace.user_uuid==user_id)).scalar_one_or_none()
    user_db = db.execute(select(Users).where(Users.user_uuid==user_id)).scalar_one_or_none()
    
    llm = load_llm()
    structured_llm = llm.with_structured_output(BasicTopicGenerationList)
    chain = prompt | structured_llm
    response:BasicTopicGenerationList = chain.invoke({"data":data.dict()})
    for topic in response.topics: 
        topic_add = TopicGeneration(
            workspace_id = workspace_db.workspace_id,
            generated_by_user_id = user_id,
            generated_by_first_name = user_db.firstname,
            generated_by_last_name = user_db.lastname,
            title=topic.title,
            angle=topic.angle,
            description=topic.description,
            channel_fit=topic.channel_fit,
            audience_fit=topic.audience_fit,
            why_it_works=topic.why_it_works,
            tags=topic.tags,
            scores=topic.scores.dict(),
        )
        db.add(topic_add)

    db.commit()


    return {"message": "Success","added topics":response}


@router.get("/get_topic")
async def get_topic(topic_id: UUID, db:Session = Depends(get_db), token= Depends(get_current_user)):
    exp_date = token.get("exp")
    if datetime.utcfromtimestamp(exp_date) <datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")

    topic_db = db.execute(select(TopicGeneration).where(TopicGeneration.topic_id==topic_id)).scalar_one_or_none()
    if not topic_db:
        raise HTTPException(status_code=401, detail="Topic not exists")
    
    return {"message": "Success"," topics":topic_db}


@router.delete("/delete_topic")
async def get_topic(topic_id: UUID, db:Session = Depends(get_db), token= Depends(get_current_user)):
    exp_date = token.get("exp")
    if datetime.utcfromtimestamp(exp_date) <datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session Expire! Login Again")
    

    topic_db = db.execute(select(TopicGeneration).where(TopicGeneration.topic_id==topic_id)).scalar_one_or_none()
    if not topic_db:
        raise HTTPException(status_code=401, detail="Topic not exists")
    
    topic_db = db.execute(Delete(TopicGeneration).where(TopicGeneration.topic_id==topic_id))
    db.commit()

    if topic_db.rowcount == 0:
        raise HTTPException(status_code=404, detail="Topic not found")

    return {"message": "Topic deleted successfully"}
