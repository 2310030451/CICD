import pytest
from app.ai.embeddings import embedding_manager


class TestEmbeddings:
    @pytest.mark.asyncio
    async def test_embedding_manager_initialization(self):
        """Test embedding manager initialization"""
        assert embedding_manager is not None
        
    @pytest.mark.asyncio
    async def test_add_documents(self):
        """Test adding documents to vector store"""
        texts = ["Test document for embedding generation"]
        metadatas = [{"test": "metadata"}]
        ids = ["test_embedding_1"]
        
        result = await embedding_manager.add_documents(texts, metadatas, ids)
        assert result is not None
        
    @pytest.mark.asyncio
    async def test_search_documents(self):
        """Test searching documents"""
        # Add test document
        texts = ["Machine learning is a field of artificial intelligence"]
        metadatas = [{"document_id": "test_doc", "user_id": "test_user_search"}]
        ids = ["search_test_1"]
        
        await embedding_manager.add_documents(texts, metadatas, ids)
        
        # Search
        results = await embedding_manager.search_documents(
            query="artificial intelligence",
            user_id="test_user_search",
            k=1
        )
        
        assert len(results) > 0
        assert results[0]["score"] > 0
        
    @pytest.mark.asyncio
    async def test_delete_documents(self):
        """Test deleting documents"""
        texts = ["Document to be deleted"]
        metadatas = [{"document_id": "test_doc_delete"}]
        ids = ["delete_test_1"]
        
        await embedding_manager.add_documents(texts, metadatas, ids)
        await embedding_manager.delete_documents(ids)
        
    @pytest.mark.asyncio
    async def test_user_isolation(self):
        """Test that users can only access their own documents"""
        # Add document for user1
        texts1 = ["User1's private document"]
        metadatas1 = [{"document_id": "doc1", "user_id": "user1"}]
        ids1 = ["user1_doc"]
        
        await embedding_manager.add_documents(texts1, metadatas1, ids1)
        
        # Search as user2 should not return user1's document
        results = await embedding_manager.search_documents(
            query="private document",
            user_id="user2",
            k=5
        )
        
        # User1's document should not be in results
        user1_docs = [r for r in results if r.get("metadata", {}).get("user_id") == "user1"]
        assert len(user1_docs) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
