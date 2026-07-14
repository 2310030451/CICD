import pytest
from app.ai.rag import rag_pipeline
from app.ai.embeddings import embedding_manager


class TestRAGPipeline:
    @pytest.mark.asyncio
    async def test_rag_initialization(self):
        """Test RAG pipeline initialization"""
        assert rag_pipeline is not None
        
    @pytest.mark.asyncio
    async def test_rag_query_with_no_documents(self):
        """Test RAG query with no documents in database"""
        response = await rag_pipeline.query(
            question="What is machine learning?",
            user_id="test_user_no_docs"
        )
        assert "answer" in response
        assert "sources" in response
        
    @pytest.mark.asyncio
    async def test_rag_query_with_documents(self):
        """Test RAG query with documents"""
        # Add test documents
        texts = [
            "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
            "Deep learning uses neural networks with multiple layers to learn patterns.",
        ]
        metadatas = [
            {"document_id": "test_doc_1", "user_id": "test_user_rag", "title": "ML Introduction"},
            {"document_id": "test_doc_1", "user_id": "test_user_rag", "title": "Deep Learning"},
        ]
        ids = ["rag_chunk_1", "rag_chunk_2"]
        
        await embedding_manager.add_documents(texts, metadatas, ids)
        
        # Query
        response = await rag_pipeline.query(
            question="What is machine learning?",
            user_id="test_user_rag"
        )
        
        assert "answer" in response
        assert "sources" in response
        assert len(response["answer"]) > 0
        
    @pytest.mark.asyncio
    async def test_rag_streaming_query(self):
        """Test RAG streaming query"""
        response = await rag_pipeline.stream_query(
            question="Explain neural networks",
            user_id="test_user_stream"
        )
        assert response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
