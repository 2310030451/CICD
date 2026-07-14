from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger


class TutorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TutorAgent",
            role="Explains concepts and provides educational guidance"
        )
        self.system_prompt = """You are an expert AI Tutor for NeuroLearn AI. Your role is to help students understand concepts clearly and effectively.

Your responsibilities:
- Explain concepts in a clear, step-by-step manner
- Adapt explanations to the student's learning style
- Use examples and analogies when helpful
- Check for understanding
- Encourage critical thinking
- Provide additional resources when needed

Always be patient, encouraging, and supportive."""
        
        self.tools = [
            {
                "name": "explain_concept",
                "description": "Explain a concept in detail",
                "parameters": ["concept", "context"],
            },
            {
                "name": "provide_example",
                "description": "Provide examples for a concept",
                "parameters": ["concept", "type"],
            },
            {
                "name": "check_understanding",
                "description": "Check student understanding",
                "parameters": ["topic"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            question = input_data.get("question", "")
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            memory_context = self.format_memory_for_context()
            
            personalized_prompt = f"{self.system_prompt}\n\n"
            personalized_prompt += f"Student Profile:\n"
            personalized_prompt += f"- Learning Style: {personalization.get('learning_style', 'mixed')}\n"
            personalized_prompt += f"- Learning Speed: {personalization.get('learning_speed', 'moderate')}\n"
            personalized_prompt += f"- Confidence Level: {personalization.get('confidence_level', 0.5)}\n"
            personalized_prompt += f"- Knowledge Gaps: {[gap['topic'] for gap in personalization.get('knowledge_gaps', [])]}\n\n"
            
            if memory_context:
                personalized_prompt += memory_context + "\n"
            
            personalized_prompt += f"Question: {question}"
            
            response = await rag_pipeline.query(
                question=question,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Question: {question}",
                "response": response["answer"],
                "sources": response.get("sources", []),
            })
            
            return {
                "agent": self.name,
                "response": response["answer"],
                "sources": response.get("sources", []),
                "personalization": {
                    "learning_style": personalization.get("learning_style"),
                    "adapted_for": personalization.get("learning_style"),
                },
            }
        except Exception as e:
            logger.error(f"TutorAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "response": "I apologize, but I encountered an error while processing your request.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools

    async def explain_concept(self, concept: str, context: Optional[str] = None) -> str:
        try:
            prompt = f"Explain the concept of {concept}"
            if context:
                prompt += f" in the context of {context}"
            
            return await self.process({"question": prompt})
        except Exception as e:
            logger.error(f"Failed to explain concept: {e}")
            return f"I couldn't explain {concept} due to an error."

    async def provide_example(self, concept: str, example_type: str = "practical") -> str:
        try:
            prompt = f"Provide a {example_type} example for {concept}"
            return await self.process({"question": prompt})
        except Exception as e:
            logger.error(f"Failed to provide example: {e}")
            return f"I couldn't provide an example for {concept} due to an error."


tutor_agent = TutorAgent()
