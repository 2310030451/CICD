import pytest
from app.agents.orchestrator import AgentOrchestrator
from app.agents.coding_agent import CodingMentorAgent
from app.agents.research_agent import ResearchAgent
from app.agents.career_agent import CareerAgent
from app.agents.analytics_agent import AnalyticsAgent


@pytest.fixture
async def orchestrator():
    return AgentOrchestrator()


class TestAgentOrchestrator:
    @pytest.mark.asyncio
    async def test_detect_intent_coding(self, orchestrator):
        """Test intent detection for coding questions"""
        query = "How do I implement a binary search in Python?"
        intent = await orchestrator.detect_intent(query)
        assert intent in ["coding", "general"]
        
    @pytest.mark.asyncio
    async def test_detect_intent_research(self, orchestrator):
        """Test intent detection for research questions"""
        query = "What are the latest developments in quantum computing?"
        intent = await orchestrator.detect_intent(query)
        assert intent in ["research", "general"]
        
    @pytest.mark.asyncio
    async def test_detect_intent_career(self, orchestrator):
        """Test intent detection for career questions"""
        query = "What skills do I need for a machine learning engineer role?"
        intent = await orchestrator.detect_intent(query)
        assert intent in ["career", "general"]
        
    @pytest.mark.asyncio
    async def test_route_to_agent(self, orchestrator):
        """Test routing to appropriate agent"""
        query = "Help me debug this code"
        agent = await orchestrator.route_to_agent(query)
        assert agent is not None


class TestCodingAgent:
    @pytest.mark.asyncio
    async def test_coding_agent_initialization(self):
        """Test coding agent initialization"""
        agent = CodingMentorAgent()
        assert agent is not None
        assert agent.name == "coding_mentor"
        
    @pytest.mark.asyncio
    async def test_coding_agent_process(self):
        """Test coding agent processing"""
        agent = CodingMentorAgent()
        response = await agent.process(
            query="Explain recursion in programming",
            user_id="test_user",
            context={}
        )
        assert response is not None
        assert "answer" in response


class TestResearchAgent:
    @pytest.mark.asyncio
    async def test_research_agent_initialization(self):
        """Test research agent initialization"""
        agent = ResearchAgent()
        assert agent is not None
        assert agent.name == "research"
        
    @pytest.mark.asyncio
    async def test_research_agent_process(self):
        """Test research agent processing"""
        agent = ResearchAgent()
        response = await agent.process(
            query="What is the current state of AI research?",
            user_id="test_user",
            context={}
        )
        assert response is not None
        assert "answer" in response


class TestCareerAgent:
    @pytest.mark.asyncio
    async def test_career_agent_initialization(self):
        """Test career agent initialization"""
        agent = CareerAgent()
        assert agent is not None
        assert agent.name == "career"
        
    @pytest.mark.asyncio
    async def test_career_agent_process(self):
        """Test career agent processing"""
        agent = CareerAgent()
        response = await agent.process(
            query="What career paths are available in data science?",
            user_id="test_user",
            context={}
        )
        assert response is not None
        assert "answer" in response


class TestAnalyticsAgent:
    @pytest.mark.asyncio
    async def test_analytics_agent_initialization(self):
        """Test analytics agent initialization"""
        agent = AnalyticsAgent()
        assert agent is not None
        assert agent.name == "analytics"
        
    @pytest.mark.asyncio
    async def test_analytics_agent_process(self):
        """Test analytics agent processing"""
        agent = AnalyticsAgent()
        response = await agent.process(
            query="Analyze my learning progress",
            user_id="test_user",
            context={"digital_twin": {"learning_style": "visual"}}
        )
        assert response is not None
        assert "answer" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
