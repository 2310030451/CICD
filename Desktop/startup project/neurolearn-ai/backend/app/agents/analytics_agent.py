from typing import Dict, List, Optional
from app.agents.base_agent import BaseAgent
from app.ai.rag import rag_pipeline
from app.learning.digital_twin import digital_twin_manager
from app.learning.lstm_model import learning_predictor
from loguru import logger


class AnalyticsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AnalyticsAgent",
            role="Analyzes learning data and provides insights"
        )
        self.system_prompt = """You are an expert Learning Analytics Specialist for NeuroLearn AI. Your role is to analyze learning data and provide actionable insights.

Your responsibilities:
- Analyze learning patterns and trends
- Identify areas for improvement
- Provide performance insights
- Suggest optimization strategies
- Compare with benchmarks
- Generate actionable recommendations
- Track progress over time

Always focus on data-driven insights that can help students improve their learning outcomes."""
        
        self.tools = [
            {
                "name": "analyze_performance",
                "description": "Analyze learning performance",
                "parameters": ["performance_data", "timeframe"],
            },
            {
                "name": "identify_patterns",
                "description": "Identify learning patterns",
                "parameters": ["activity_data", "metrics"],
            },
            {
                "name": "generate_insights",
                "description": "Generate actionable insights",
                "parameters": ["data", "focus_areas"],
            },
        ]

    def get_system_prompt(self) -> str:
        return self.system_prompt

    async def process(self, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        try:
            self.update_last_used()
            
            user_id = input_data.get("user_id")
            data = input_data.get("data", {})
            question = input_data.get("question", "")
            document_ids = input_data.get("document_ids")
            
            digital_twin = digital_twin_manager.get_twin(user_id)
            personalization = digital_twin.get_personalization_profile()
            
            prompt = f"Analyze the following learning data: {data}. "
            prompt += f"Student profile: "
            prompt += f"- Learning speed: {personalization.get('learning_speed')} "
            prompt += f"- Confidence level: {personalization.get('confidence_level'):.2f} "
            prompt += f"- Memory retention: {personalization.get('memory_retention'):.2f} "
            prompt += f"- Knowledge gaps: {[gap['topic'] for gap in personalization.get('knowledge_gaps', [])]}. "
            if question:
                prompt += f"Question: {question}. "
            prompt += "Provide data-driven insights and actionable recommendations."
            
            response = await rag_pipeline.query(
                question=prompt,
                user_id=user_id,
                document_ids=document_ids,
            )
            
            self.add_to_memory({
                "content": f"Analyzed learning data for user",
                "data_summary": str(data)[:200],
            })
            
            return {
                "agent": self.name,
                "response": response["answer"],
                "personalization": personalization,
            }
        except Exception as e:
            logger.error(f"AnalyticsAgent processing failed: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "response": "I apologize, but I encountered an error while analyzing the data.",
            }

    def get_tools(self) -> List[Dict]:
        return self.tools


analytics_agent = AnalyticsAgent()
