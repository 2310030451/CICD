from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.study_plan import StudyPlanCreate, StudyPlanUpdate, StudyPlan
from app.core.database import get_database
from app.core.auth import decode_token
from loguru import logger
from datetime import datetime


router = APIRouter()


async def get_current_user_id(token: str) -> str:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return payload.get("user_id")


@router.post("/", response_model=StudyPlan)
async def create_revision_plan(
    plan: StudyPlanCreate,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        plan_dict = plan.model_dump()
        plan_dict["user_id"] = user_id
        plan_dict["created_at"] = datetime.utcnow()
        plan_dict["updated_at"] = datetime.utcnow()
        
        result = await db.revision_plans.insert_one(plan_dict)
        plan_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Created revision plan for user {user_id}")
        return StudyPlan(**plan_dict)
    except Exception as e:
        logger.error(f"Failed to create revision plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to create revision plan")


@router.get("/", response_model=List[StudyPlan])
async def get_revision_plans(
    status: str = None,
    limit: int = 20,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        plans = await db.revision_plans.find(query).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        return [StudyPlan(**plan) for plan in plans]
    except Exception as e:
        logger.error(f"Failed to get revision plans: {e}")
        raise HTTPException(status_code=500, detail="Failed to get revision plans")


@router.put("/{plan_id}", response_model=StudyPlan)
async def update_revision_plan(
    plan_id: str,
    update: StudyPlanUpdate,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        update_dict = update.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        result = await db.revision_plans.update_one(
            {"_id": plan_id, "user_id": user_id},
            {"$set": update_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Revision plan not found")
        
        plan = await db.revision_plans.find_one({"_id": plan_id})
        return StudyPlan(**plan)
    except Exception as e:
        logger.error(f"Failed to update revision plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to update revision plan")


@router.delete("/{plan_id}")
async def delete_revision_plan(
    plan_id: str,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        result = await db.revision_plans.delete_one(
            {"_id": plan_id, "user_id": user_id}
        )
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Revision plan not found")
        
        return {"deleted": True}
    except Exception as e:
        logger.error(f"Failed to delete revision plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete revision plan")
