from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger


class QuizAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="QuizAgent",
            role="Creates quizzes and assessments"
        )
        self.system_prompt = """You are an expert Quiz Creator for NeuroLearn AI. Your role is to create effective quizzes that test understanding and reinforce learning.

Your responsibilities:
- Create questions at appropriate difficulty levels
- Include multiple question types (multiple choice, true/false, short answer)
- Ensure questions are clear and unambiguous
- Provide correct answers and explanations
- Adapt difficulty based on student performance
- Cover key concepts thoroughly

Always focus on learning outcomes and knowledge retention."""
        
        self.tools = [
            {
                "name": "create_quiz",
                "description": "Create a quiz on a topic",
                "parameters": ["topic", "question_count", "difficulty"],
            },
            {
                "name": "generate_question",
                "description": "Generate a single question",
                "parameters": ["topic", "question_type"],
            },
            {
                "name": "assess_difficulty",
                "description": "Assess appropriate difficulty level",
                "parameters": ["topic", "student_level"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            topic = input_data.get("topic", "")
            question_count = input_data.get("question_count", 5)
            difficulty = input_data.get("difficulty", "medium")
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            confidence = personalization.get("confidence_level", 0.5)
            
            if confidence < 0.4 and difficulty == "hard":
                difficulty = "medium"
            elif confidence > 0.8 and difficulty == "easy":
                difficulty = "medium"
            
            prompt = f"Create a {question_count}-question quiz on {topic} at {difficulty} difficulty level. "
            prompt += f"Include multiple choice questions with correct answers and explanations."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Created quiz on {topic}",
                "difficulty": difficulty,
                "question_count": question_count,
            })
            
            return {
                "agent": self.name,
                "quiz": response["answer"],
                "topic": topic,
                "difficulty": difficulty,
                "question_count": question_count,
                "adapted_for_confidence": confidence,
            }
        except Exception as e:
            logger.error(f"QuizAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "quiz": "I apologize, but I encountered an error while creating the quiz.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


quiz_agent = QuizAgent()
