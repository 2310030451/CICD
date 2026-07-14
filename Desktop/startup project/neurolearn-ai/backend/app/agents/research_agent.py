from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from loguru import logger


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            role="Summarizes research papers and academic content"
        )
        self.system_prompt = """You are an expert Research Assistant for NeuroLearn AI. Your role is to help students understand research papers and academic content.

Your responsibilities:
- Summarize research papers clearly
- Explain key findings and methodologies
- Identify important concepts and terminology
- Connect research to practical applications
- Suggest related research or readings
- Help with literature reviews
- Explain statistical analyses

Always focus on clarity and helping students understand complex academic content."""
        
        self.tools = [
            {
                "name": "summarize_paper",
                "description": "Summarize a research paper",
                "parameters": ["paper_content", "focus_areas"],
            },
            {
                "name": "explain_findings",
                "description": "Explain research findings",
                "parameters": ["findings", "context"],
            },
            {
                "name": "suggest_related",
                "description": "Suggest related research",
                "parameters": ["topic", "field"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            content = input_data.get("content", "")
            question = input_data.get("question", "")
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            confidence = personalization.get("confidence_level", 0.5)
            
            prompt = f"Analyze and summarize the following research content: {content[:1000]}. "
            if question:
                prompt += f"Question: {question}. "
            prompt += f"Student confidence level: {confidence:.2f}. "
            prompt += "Provide clear explanations and highlight key findings."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Summarized research content",
                "confidence_level": confidence,
            })
            
            return {
                "agent": self.name,
                "response": response["answer"],
                "confidence_level": confidence,
            }
        except Exception as e:
            logger.error(f"ResearchAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "response": "I apologize, but I encountered an error while processing the research content.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


research_agent = ResearchAgent()
