from typing import Dict, List, Optional, Any
from app.agents.tutor_agent import tutor_agent
from app.agents.quiz_agent import quiz_agent
from app.agents.planner_agent import planner_agent
from app.agents.revision_agent import revision_agent
from app.agents.coding_agent import coding_mentor_agent
from app.agents.research_agent import research_agent
from app.agents.career_agent import career_agent
from app.agents.analytics_agent import analytics_agent
from app.config import settings
from loguru import logger


class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            "tutor": tutor_agent,
            "quiz": quiz_agent,
            "planner": planner_agent,
            "revision": revision_agent,
            "coding": coding_mentor_agent,
            "research": research_agent,
            "career": career_agent,
            "analytics": analytics_agent,
        }
        self.agent_routing_rules = self._initialize_routing_rules()

    def _initialize_routing_rules(self) -> Dict[str, List[str]]:
        return {
            "explain_concept": ["tutor"],
            "create_quiz": ["quiz"],
            "study_schedule": ["planner"],
            "revision_plan": ["revision"],
            "code_help": ["coding"],
            "research_summary": ["research"],
            "career_advice": ["career"],
            "analytics": ["analytics"],
            "general_question": ["tutor", "analytics"],
            "learning_guidance": ["tutor", "planner"],
            "exam_preparation": ["quiz", "revision", "planner"],
        }

    async def route_request(self, request: Dict) -> Dict:
        try:
            if not settings.enable_agent_orchestration:
                return await self._default_routing(request)
            
            intent = self._detect_intent(request)
            preferred_agents = self.agent_routing_rules.get(intent, ["tutor"])
            
            results = []
            for agent_name in preferred_agents:
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    result = await agent.process(request)
                    results.append(result)
            
            if len(results) == 1:
                return results[0]
            else:
                return self._merge_results(results, intent)
        except Exception as e:
            logger.error(f"Agent orchestration failed: {e}")
            return await self._default_routing(request)

    def _detect_intent(self, request: Dict) -> str:
        try:
            question = request.get("question", "").lower()
            request_type = request.get("type", "")
            
            if request_type:
                return request_type
            
            keywords = {
                "explain_concept": ["explain", "what is", "how does", "concept", "understand"],
                "create_quiz": ["quiz", "test", "assessment", "practice question"],
                "study_schedule": ["schedule", "plan", "study plan", "daily"],
                "revision_plan": ["revision", "review", "spaced repetition"],
                "code_help": ["code", "programming", "debug", "function", "algorithm"],
                "research_summary": ["research", "paper", "study", "academic"],
                "career_advice": ["career", "job", "internship", "resume", "interview"],
                "analytics": ["analyze", "performance", "progress", "statistics"],
            }
            
            for intent, words in keywords.items():
                if any(word in question for word in words):
                    return intent
            
            return "general_question"
        except Exception as e:
            logger.error(f"Intent detection failed: {e}")
            return "general_question"

    async def _default_routing(self, request: Dict) -> Dict:
        try:
            return await tutor_agent.process(request)
        except Exception as e:
            logger.error(f"Default routing failed: {e}")
            return {
                "agent": "orchestrator",
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request.",
            }

    def _merge_results(self, results: List[Dict], intent: str) -> Dict:
        try:
            merged = {
                "agent": "orchestrator",
                "intent": intent,
                "responses": [],
                "primary_response": None,
            }
            
            for result in results:
                if "response" in result:
                    merged["responses"].append({
                        "agent": result.get("agent"),
                        "response": result.get("response"),
                    })
            
            if merged["responses"]:
                merged["primary_response"] = merged["responses"][0]["response"]
            
            return merged
        except Exception as e:
            logger.error(f"Result merging failed: {e}")
            return {
                "agent": "orchestrator",
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request.",
            }

    def get_available_agents(self) -> List[Dict]:
        try:
            return [
                {
                    "name": name,
                    "role": agent.role,
                    "tools": agent.get_tools(),
                    "stats": agent.get_usage_stats(),
                }
                for name, agent in self.agents.items()
            ]
        except Exception as e:
            logger.error(f"Failed to get available agents: {e}")
            return []

    async def execute_agent(self, agent_name: str, request: Dict) -> Dict:
        try:
            if agent_name not in self.agents:
                return {
                    "agent": "orchestrator",
                    "error": f"Agent {agent_name} not found",
                    "response": f"The requested agent {agent_name} is not available.",
                }
            
            agent = self.agents[agent_name]
            return await agent.process(request)
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return {
                "agent": agent_name,
                "error": str(e),
                "response": f"I apologize, but I encountered an error while processing your request with {agent_name}.",
            }

    def get_agent_memory(self, agent_name: str, limit: int = 10) -> List[Dict]:
        try:
            if agent_name not in self.agents:
                return []
            
            agent = self.agents[agent_name]
            return agent.get_memory(limit)
        except Exception as e:
            logger.error(f"Failed to get agent memory: {e}")
            return []

    def clear_agent_memory(self, agent_name: str) -> bool:
        try:
            if agent_name not in self.agents:
                return False
            
            agent = self.agents[agent_name]
            agent.clear_memory()
            return True
        except Exception as e:
            logger.error(f"Failed to clear agent memory: {e}")
            return False

    def get_system_status(self) -> Dict:
        try:
            return {
                "orchestration_enabled": settings.enable_agent_orchestration,
                "total_agents": len(self.agents),
                "available_agents": list(self.agents.keys()),
                "agent_stats": {name: agent.get_usage_stats() for name, agent in self.agents.items()},
            }
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {}


agent_orchestrator = AgentOrchestrator()
