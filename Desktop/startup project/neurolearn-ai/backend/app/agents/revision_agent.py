from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger
from datetime import datetime, timedelta


class RevisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RevisionAgent",
            role="Creates revision plans and schedules"
        )
        self.system_prompt = """You are an expert Revision Planner for NeuroLearn AI. Your role is to create effective revision plans that maximize knowledge retention.

Your responsibilities:
- Identify topics needing revision based on performance
- Create spaced repetition schedules
- Prioritize weak areas while maintaining strengths
- Optimize revision timing for memory retention
- Include active recall techniques
- Balance revision with new learning
- Adapt to forgetting curves

Always focus on long-term retention and understanding."""
        
        self.tools = [
            {
                "name": "create_revision_plan",
                "description": "Create a revision plan",
                "parameters": ["topics", "exam_date", "current_performance"],
            },
            {
                "name": "schedule_spaced_repetition",
                "description": "Schedule spaced repetition sessions",
                "parameters": ["topic", "mastery_level", "last_reviewed"],
            },
            {
                "name": "identify_revision_priorities",
                "description": "Identify topics needing revision",
                "parameters": ["performance_data", "time_available"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            topics = input_data.get("topics", [])
            exam_date = input_data.get("exam_date")
            time_available = input_data.get("time_available", 7)
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            knowledge_gaps = personalization.get("knowledge_gaps", [])
            memory_retention = personalization.get("memory_retention", 0.7)
            revision_patterns = personalization.get("revision_patterns", {})
            
            priority_topics = [gap["topic"] for gap in knowledge_gaps] if knowledge_gaps else topics
            
            prompt = f"Create a revision plan for {time_available} days. "
            prompt += f"Priority topics: {', '.join(priority_topics) if priority_topics else 'all topics'}. "
            if exam_date:
                prompt += f"Exam date: {exam_date}. "
            prompt += f"Student profile: "
            prompt += f"- Memory retention: {memory_retention:.2f} "
            prompt += f"- Knowledge gaps: {[gap['topic'] for gap in knowledge_gaps]} "
            prompt += f"- Revision patterns: {revision_patterns}. "
            prompt += "Use spaced repetition and optimize for long-term retention."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Created revision plan for {time_available} days",
                "priority_topics": priority_topics,
                "memory_retention": memory_retention,
            })
            
            return {
                "agent": self.name,
                "revision_plan": response["answer"],
                "priority_topics": priority_topics,
                "time_available": time_available,
                "memory_retention": memory_retention,
                "knowledge_gaps": knowledge_gaps,
            }
        except Exception as e:
            logger.error(f"RevisionAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "revision_plan": "I apologize, but I encountered an error while creating the revision plan.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


revision_agent = RevisionAgent()
