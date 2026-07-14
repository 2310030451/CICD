from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger


class CareerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CareerAgent",
            role="Suggests internships, jobs, and learning paths"
        )
        self.system_prompt = """You are an expert Career Advisor for NeuroLearn AI. Your role is to help students plan their career paths and find opportunities.

Your responsibilities:
- Suggest career paths based on skills and interests
- Recommend internships and job opportunities
- Create learning roadmaps for career goals
- Identify skill gaps for target roles
- Suggest certifications and courses
- Provide industry insights
- Help with resume and interview preparation

Always focus on practical, actionable advice tailored to the student's profile."""
        
        self.tools = [
            {
                "name": "suggest_career_paths",
                "description": "Suggest career paths",
                "parameters": ["skills", "interests", "education"],
            },
            {
                "name": "find_opportunities",
                "description": "Find internships and jobs",
                "parameters": ["role", "location", "experience"],
            },
            {
                "name": "create_roadmap",
                "description": "Create learning roadmap",
                "parameters": ["target_role", "current_skills", "timeline"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            skills = input_data.get("skills", [])
            interests = input_data.get("interests", [])
            target_role = input_data.get("target_role", "")
            question = input_data.get("question", "")
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            strengths = personalization.get("strengths", [])
            weaknesses = personalization.get("weaknesses", [])
            
            prompt = f"Provide career guidance. "
            if target_role:
                prompt += f"Target role: {target_role}. "
            if skills:
                prompt += f"Current skills: {', '.join(skills)}. "
            if interests:
                prompt += f"Interests: {', '.join(interests)}. "
            prompt += f"Strengths: {[s['topic'] for s in strengths]}. "
            prompt += f"Areas to improve: {[w['topic'] for w in weaknesses]}. "
            if question:
                prompt += f"Question: {question}. "
            prompt += "Provide actionable advice and specific recommendations."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Provided career guidance for {target_role or 'general'}",
                "skills": skills,
                "strengths": strengths,
            })
            
            return {
                "agent": self.name,
                "response": response["answer"],
                "target_role": target_role,
                "strengths": strengths,
                "weaknesses": weaknesses,
            }
        except Exception as e:
            logger.error(f"CareerAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "response": "I apologize, but I encountered an error while providing career guidance.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


career_agent = CareerAgent()
