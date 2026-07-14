from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.agent_memory import AgentMemoryCreate, AgentMemory
from app.core.database import get_database
from app.core.auth import decode_token
from app.agents.orchestrator import agent_orchestrator
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


@router.post("/route")
async def route_to_agent(
    request: dict,
    user_id: str = Depends(get_current_user_id)
):
    try:
        request["user_id"] = user_id
        result = await agent_orchestrator.route_request(request)
        return result
    except Exception as e:
        logger.error(f"Failed to route request: {e}")
        raise HTTPException(status_code=500, detail="Failed to route request")


@router.get("/agents")
async def get_available_agents():
    try:
        agents = agent_orchestrator.get_available_agents()
        return {"agents": agents}
    except Exception as e:
        logger.error(f"Failed to get available agents: {e}")
        raise HTTPException(status_code=500, detail="Failed to get available agents")


@router.post("/execute/{agent_name}")
async def execute_agent(
    agent_name: str,
    request: dict,
    user_id: str = Depends(get_current_user_id)
):
    try:
        request["user_id"] = user_id
        result = await agent_orchestrator.execute_agent(agent_name, request)
        return result
    except Exception as e:
        logger.error(f"Failed to execute agent: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute agent")


@router.get("/memory/{agent_name}", response_model=List[AgentMemory])
async def get_agent_memory(
    agent_name: str,
    limit: int = 10,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        memory = await db.agent_memory.find(
            {"user_id": user_id, "agent_name": agent_name}
        ).sort("timestamp", -1).limit(limit).to_list(length=limit)
        
        return [AgentMemory(**mem) for mem in memory]
    except Exception as e:
        logger.error(f"Failed to get agent memory: {e}")
        raise HTTPException(status_code=500, detail="Failed to get agent memory")


@router.delete("/memory/{agent_name}")
async def clear_agent_memory(
    agent_name: str,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        result = await db.agent_memory.delete_many(
            {"user_id": user_id, "agent_name": agent_name}
        )
        
        agent_orchestrator.clear_agent_memory(agent_name)
        
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        logger.error(f"Failed to clear agent memory: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear agent memory")
