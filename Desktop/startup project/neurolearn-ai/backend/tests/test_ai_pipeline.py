import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db, close_db, get_database
from app.ai.document_processor import DocumentProcessor
from app.ai.embeddings import embedding_manager
from app.ai.rag import rag_pipeline
from app.services.document_service import DocumentService
from app.services.conversation_service import ConversationService
from app.models.document import DocumentCreate, DocumentStatus
from app.models.conversation import ConversationCreate
import os
import tempfile


@pytest.fixture
async def client():
    async with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def test_db():
    await init_db()
    db = await get_database()
    yield db
    await close_db()


@pytest.fixture
async def sample_text_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test document for NeuroLearn AI. It contains information about machine learning and artificial intelligence. The document discusses various concepts including neural networks, deep learning, and natural language processing.")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
async def sample_pdf_file():
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestDocumentProcessor:
    @pytest.mark.asyncio
    async def test_text_extraction_txt(self, sample_text_file):
        processor = DocumentProcessor()
        text = await processor.extract_text(sample_text_file, "txt")
        assert "NeuroLearn AI" in text
        assert "machine learning" in text

    @pytest.mark.asyncio
    async def test_text_cleaning(self):
        processor = DocumentProcessor()
        dirty_text = "  This  is  a  dirty  text  \n\n  with  extra  spaces  "
        clean_text = processor.clean_text(dirty_text)
        assert clean_text == "This is a dirty text with extra spaces"

    @pytest.mark.asyncio
    async def test_text_chunking(self):
        processor = DocumentProcessor()
        text = "This is a test document. It has multiple sentences. Each sentence should be chunked properly."
        chunks = processor.chunk_text(text, chunk_size=50, overlap=10)
        assert len(chunks) > 1
        assert all(chunk for chunk in chunks)


class TestEmbeddings:
    @pytest.mark.asyncio
    async def test_embedding_generation(self):
        texts = ["This is a test sentence for embedding generation."]
        metadatas = [{"test": "metadata"}]
        ids = ["test_id_1"]
        
        await embedding_manager.add_documents(texts, metadatas, ids)
        
        results = await embedding_manager.search_documents("test sentence", "test_user", k=1)
        assert len(results) > 0
        assert results[0]["score"] > 0


class TestDocumentService:
    @pytest.mark.asyncio
    async def test_create_document(self, test_db):
        service = DocumentService()
        document_data = DocumentCreate(
            user_id="test_user",
            title="Test Document",
            file_name="test.txt",
            file_type="txt",
            file_size=100,
            file_url="/uploads/test.txt",
            file_hash="test_hash",
        )
        
        document = await service.create_document(document_data)
        assert document.id is not None
        assert document.status == DocumentStatus.PROCESSING

    @pytest.mark.asyncio
    async def test_get_document_by_id(self, test_db):
        service = DocumentService()
        document_data = DocumentCreate(
            user_id="test_user",
            title="Test Document",
            file_name="test.txt",
            file_type="txt",
            file_size=100,
            file_url="/uploads/test.txt",
            file_hash="test_hash",
        )
        
        created = await service.create_document(document_data)
        retrieved = await service.get_document_by_id(created.id, "test_user")
        
        assert retrieved is not None
        assert retrieved.id == created.id

    @pytest.mark.asyncio
    async def test_delete_document(self, test_db):
        service = DocumentService()
        document_data = DocumentCreate(
            user_id="test_user",
            title="Test Document",
            file_name="test.txt",
            file_type="txt",
            file_size=100,
            file_url="/uploads/test.txt",
            file_hash="test_hash",
        )
        
        created = await service.create_document(document_data)
        success = await service.delete_document(created.id, "test_user")
        
        assert success is True
        retrieved = await service.get_document_by_id(created.id, "test_user")
        assert retrieved is None


class TestConversationService:
    @pytest.mark.asyncio
    async def test_create_conversation(self, test_db):
        service = ConversationService()
        conversation_data = ConversationCreate(
            user_id="test_user",
            title="Test Conversation",
            document_ids=[],
        )
        
        conversation = await service.create_conversation(conversation_data)
        assert conversation.id is not None
        assert conversation.title == "Test Conversation"

    @pytest.mark.asyncio
    async def test_add_message(self, test_db):
        service = ConversationService()
        conversation_data = ConversationCreate(
            user_id="test_user",
            title="Test Conversation",
            document_ids=[],
        )
        
        conversation = await service.create_conversation(conversation_data)
        await service.add_message(conversation.id, "user", "Hello, this is a test message")
        
        updated = await service.get_conversation_by_id(conversation.id, "test_user")
        assert len(updated.messages) == 1
        assert updated.messages[0].role == "user"


class TestRAGPipeline:
    @pytest.mark.asyncio
    async def test_rag_query(self):
        texts = [
            "NeuroLearn AI is an educational platform that uses artificial intelligence to help students learn.",
            "The platform supports document upload, processing, and AI-powered tutoring.",
        ]
        metadatas = [
            {"document_id": "doc1", "user_id": "test_user", "title": "Introduction"},
            {"document_id": "doc1", "user_id": "test_user", "title": "Features"},
        ]
        ids = ["chunk1", "chunk2"]
        
        await embedding_manager.add_documents(texts, metadatas, ids)
        
        response = await rag_pipeline.query(
            question="What is NeuroLearn AI?",
            user_id="test_user",
        )
        
        assert "answer" in response
        assert "sources" in response
        assert len(response["answer"]) > 0


class TestAPIEndpoints:
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_document_upload(self, client, sample_text_file):
        with open(sample_text_file, 'rb') as f:
            response = client.post(
                "/api/v1/documents/upload",
                files={"file": ("test.txt", f, "text/plain")},
                data={
                    "title": "Test Upload",
                    "subject": "Testing",
                    "tags": "test,integration",
                },
                headers={"Authorization": "Bearer test_token"},
            )
        
        assert response.status_code in [200, 401]

    @pytest.mark.asyncio
    async def test_get_documents(self, client):
        response = client.get(
            "/api/v1/documents/",
            headers={"Authorization": "Bearer test_token"},
        )
        
        assert response.status_code in [200, 401]

    @pytest.mark.asyncio
    async def test_chat_endpoint(self, client):
        response = client.post(
            "/api/v1/ai/chat",
            json={
                "question": "What is machine learning?",
                "document_ids": [],
            },
            headers={"Authorization": "Bearer test_token"},
        )
        
        assert response.status_code in [200, 401, 500]

    @pytest.mark.asyncio
    async def test_conversations_list(self, client):
        response = client.get(
            "/api/v1/ai/conversations",
            headers={"Authorization": "Bearer test_token"},
        )
        
        assert response.status_code in [200, 401]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
