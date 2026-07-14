from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger


class CodingMentorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CodingMentorAgent",
            role="Explains code and provides programming guidance"
        )
        self.system_prompt = """You are an expert Coding Mentor for NeuroLearn AI. Your role is to help students understand programming concepts and improve their coding skills.

Your responsibilities:
- Explain code clearly and thoroughly
- Debug code and explain errors
- Suggest improvements and best practices
- Teach programming concepts step-by-step
- Provide code examples and explanations
- Help with algorithm design
- Guide problem-solving approaches

Always be patient and focus on helping the student learn, not just providing answers."""
        
        self.tools = [
            {
                "name": "explain_code",
                "description": "Explain code functionality",
                "parameters": ["code", "language"],
            },
            {
                "name": "debug_code",
                "description": "Debug and fix code issues",
                "parameters": ["code", "error_message"],
            },
            {
                "name": "suggest_improvements",
                "description": "Suggest code improvements",
                "parameters": ["code", "context"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            code = input_data.get("code", "")
            language = input_data.get("language", "python")
            question = input_data.get("question", "")
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            learning_speed = personalization.get("learning_speed", "moderate")
            
            prompt = f"Explain the following {language} code: {code}. "
            if question:
                prompt += f"Question: {question}. "
            prompt += f"Student learning speed: {learning_speed}. "
            prompt += "Provide clear explanations and examples."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Explained {language} code",
                "language": language,
                "learning_speed": learning_speed,
            })
            
            return {
                "agent": self.name,
                "response": response["answer"],
                "language": language,
                "learning_speed": learning_speed,
            }
        except Exception as e:
            logger.error(f"CodingMentorAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "response": "I apologize, but I encountered an error while processing your code.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


coding_mentor_agent = CodingMentorAgent()
