import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.database import init_db, close_db, get_database
from app.models.user import UserCreate, UserRole
from app.models.document import DocumentCreate, DocumentStatus
import os


@pytest.fixture
async def test_db():
    """Fixture for test database connection"""
    await init_db()
    db = await get_database()
    yield db
    await close_db()


class TestDatabaseConnection:
    @pytest.mark.asyncio
    async def test_database_connection(self, test_db):
        """Test that database connection is established"""
        assert test_db is not None
        # Test ping
        await test_db.command('ping')
        
    @pytest.mark.asyncio
    async def test_collection_exists(self, test_db):
        """Test that required collections exist"""
        collections = await test_db.list_collection_names()
        assert "users" in collections
        assert "documents" in collections
        assert "conversations" in collections


class TestUserCRUD:
    @pytest.mark.asyncio
    async def test_create_user(self, test_db):
        """Test user creation"""
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            firebase_uid="test_firebase_uid",
            role=UserRole.STUDENT
        )
        
        result = await test_db.users.insert_one(user_data.dict())
        assert result.inserted_id is not None
        
    @pytest.mark.asyncio
    async def test_get_user_by_email(self, test_db):
        """Test retrieving user by email"""
        user_data = UserCreate(
            email="test2@example.com",
            name="Test User 2",
            firebase_uid="test_firebase_uid_2",
            role=UserRole.STUDENT
        )
        
        await test_db.users.insert_one(user_data.dict())
        
        user = await test_db.users.find_one({"email": "test2@example.com"})
        assert user is not None
        assert user["name"] == "Test User 2"
        
    @pytest.mark.asyncio
    async def test_update_user(self, test_db):
        """Test updating user"""
        user_data = UserCreate(
            email="test3@example.com",
            name="Test User 3",
            firebase_uid="test_firebase_uid_3",
            role=UserRole.STUDENT
        )
        
        result = await test_db.users.insert_one(user_data.dict())
        user_id = result.inserted_id
        
        await test_db.users.update_one(
            {"_id": user_id},
            {"$set": {"name": "Updated Name"}}
        )
        
        updated_user = await test_db.users.find_one({"_id": user_id})
        assert updated_user["name"] == "Updated Name"
        
    @pytest.mark.asyncio
    async def test_delete_user(self, test_db):
        """Test deleting user"""
        user_data = UserCreate(
            email="test4@example.com",
            name="Test User 4",
            firebase_uid="test_firebase_uid_4",
            role=UserRole.STUDENT
        )
        
        result = await test_db.users.insert_one(user_data.dict())
        user_id = result.inserted_id
        
        await test_db.users.delete_one({"_id": user_id})
        
        deleted_user = await test_db.users.find_one({"_id": user_id})
        assert deleted_user is None


class TestDocumentCRUD:
    @pytest.mark.asyncio
    async def test_create_document(self, test_db):
        """Test document creation"""
        document_data = DocumentCreate(
            user_id="test_user",
            title="Test Document",
            file_name="test.pdf",
            file_type="pdf",
            file_size=1024,
            file_url="/uploads/test.pdf",
            file_hash="test_hash_123"
        )
        
        result = await test_db.documents.insert_one(document_data.dict())
        assert result.inserted_id is not None
        
    @pytest.mark.asyncio
    async def test_get_documents_by_user(self, test_db):
        """Test retrieving documents by user"""
        document_data = DocumentCreate(
            user_id="test_user_2",
            title="Test Document 2",
            file_name="test2.pdf",
            file_type="pdf",
            file_size=2048,
            file_url="/uploads/test2.pdf",
            file_hash="test_hash_456"
        )
        
        await test_db.documents.insert_one(document_data.dict())
        
        documents = await test_db.documents.find({"user_id": "test_user_2"}).to_list(length=10)
        assert len(documents) > 0
        assert documents[0]["title"] == "Test Document 2"
        
    @pytest.mark.asyncio
    async def test_update_document_status(self, test_db):
        """Test updating document status"""
        document_data = DocumentCreate(
            user_id="test_user_3",
            title="Test Document 3",
            file_name="test3.pdf",
            file_type="pdf",
            file_size=3072,
            file_url="/uploads/test3.pdf",
            file_hash="test_hash_789"
        )
        
        result = await test_db.documents.insert_one(document_data.dict())
        document_id = result.inserted_id
        
        await test_db.documents.update_one(
            {"_id": document_id},
            {"$set": {"status": DocumentStatus.COMPLETED.value}}
        )
        
        updated_document = await test_db.documents.find_one({"_id": document_id})
        assert updated_document["status"] == DocumentStatus.COMPLETED.value


class TestIndexes:
    @pytest.mark.asyncio
    async def test_user_email_index(self, test_db):
        """Test that email index exists on users collection"""
        indexes = await test_db.users.index_information()
        assert "email_1" in indexes or any("email" in str(idx) for idx in indexes.values())
        
    @pytest.mark.asyncio
    async def test_document_user_id_index(self, test_db):
        """Test that user_id index exists on documents collection"""
        indexes = await test_db.documents.index_information()
        assert "user_id_1" in indexes or any("user_id" in str(idx) for idx in indexes.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
