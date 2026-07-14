from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger
from datetime import datetime, timedelta


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            role="Creates daily study schedules and learning plans"
        )
        self.system_prompt = """You are an expert Study Planner for NeuroLearn AI. Your role is to create personalized study schedules that optimize learning outcomes.

Your responsibilities:
- Create realistic daily study schedules
- Balance different subjects and topics
- Include breaks and review sessions
- Adapt to student's available time and preferences
- Consider learning speed and attention span
- Align with exam dates and deadlines
- Optimize for memory retention

Always create schedules that are achievable and sustainable."""
        
        self.tools = [
            {
                "name": "create_daily_schedule",
                "description": "Create a daily study schedule",
                "parameters": ["available_hours", "subjects", "preferences"],
            },
            {
                "name": "create_weekly_plan",
                "description": "Create a weekly study plan",
                "parameters": ["goals", "time_constraints", "priorities"],
            },
            {
                "name": "optimize_schedule",
                "description": "Optimize existing schedule",
                "parameters": ["current_schedule", "performance_data"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            available_hours = input_data.get("available_hours", 4)
            subjects = input_data.get("subjects", [])
            goals = input_data.get("goals", [])
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            attention_span = personalization.get("attention_span_minutes", 30)
            preferred_time = personalization.get("preferred_study_time", "flexible")
            learning_speed = personalization.get("learning_speed", "moderate")
            
            prompt = f"Create a daily study schedule for {available_hours} hours. "
            prompt += f"Subjects: {', '.join(subjects) if subjects else 'general studies'}. "
            prompt += f"Goals: {', '.join(goals) if goals else 'general improvement'}. "
            prompt += f"Student preferences: "
            prompt += f"- Attention span: {attention_span} minutes "
            prompt += f"- Preferred study time: {preferred_time} "
            prompt += f"- Learning speed: {learning_speed}. "
            prompt += "Include breaks and optimize for memory retention."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Created schedule for {available_hours} hours",
                "subjects": subjects,
                "optimized_for": preferred_time,
            })
            
            return {
                "agent": self.name,
                "schedule": response["answer"],
                "available_hours": available_hours,
                "attention_span": attention_span,
                "preferred_time": preferred_time,
                "learning_speed": learning_speed,
            }
        except Exception as e:
            logger.error(f"PlannerAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "schedule": "I apologize, but I encountered an error while creating the schedule.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


planner_agent = PlannerAgent()
