from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.digital_twin import DigitalTwinCreate, DigitalTwinUpdate, DigitalTwin
from app.core.database import get_database
from app.core.auth import decode_token
from app.learning.digital_twin import digital_twin_manager
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


@router.get("/", response_model=DigitalTwin)
async def get_digital_twin(
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        twin = await db.digital_twins.find_one({"user_id": user_id})
        
        if not twin:
            in_memory_twin = digital_twin_manager.get_twin(user_id)
            twin_data = in_memory_twin.to_dict()
            twin_data["created_at"] = datetime.utcnow()
            twin_data["last_updated"] = datetime.utcnow()
            
            result = await db.digital_twins.insert_one(twin_data)
            twin_data["_id"] = str(result.inserted_id)
            return DigitalTwin(**twin_data)
        
        return DigitalTwin(**twin)
    except Exception as e:
        logger.error(f"Failed to get digital twin: {e}")
        raise HTTPException(status_code=500, detail="Failed to get digital twin")


@router.put("/", response_model=DigitalTwin)
async def update_digital_twin(
    update: DigitalTwinUpdate,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        update_dict = update.model_dump(exclude_unset=True)
        update_dict["last_updated"] = datetime.utcnow()
        
        result = await db.digital_twins.update_one(
            {"user_id": user_id},
            {"$set": update_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        twin = await db.digital_twins.find_one({"user_id": user_id})
        return DigitalTwin(**twin)
    except Exception as e:
        logger.error(f"Failed to update digital twin: {e}")
        raise HTTPException(status_code=500, detail="Failed to update digital twin")
