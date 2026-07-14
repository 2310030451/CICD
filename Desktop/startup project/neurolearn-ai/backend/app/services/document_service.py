from datetime import datetime
from typing import Optional, List
from app.models.document import DocumentCreate, DocumentUpdate, DocumentInDB, DocumentStatus
from app.core.database import get_database
from app.ai.document_processor import DocumentProcessor
from app.ai.embeddings import embedding_manager
from app.config import settings
from loguru import logger
import os


class DocumentService:
    def __init__(self):
        self.db = None
        self.document_processor = DocumentProcessor()

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_document(self, document_data: DocumentCreate) -> DocumentInDB:
        db = await self.get_database()
        document_dict = document_data.model_dump()
        document_dict["status"] = DocumentStatus.PROCESSING
        document_dict["chunk_count"] = 0
        document_dict["created_at"] = datetime.utcnow()
        document_dict["updated_at"] = datetime.utcnow()
        
        result = await db.documents.insert_one(document_dict)
        document_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Document created with ID: {result.inserted_id}")
        return DocumentInDB(**document_dict)

    async def get_document_by_id(self, document_id: str, user_id: str) -> Optional[DocumentInDB]:
        db = await self.get_database()
        document_doc = await db.documents.find_one({"_id": document_id, "user_id": user_id})
        
        if document_doc:
            document_doc["_id"] = str(document_doc["_id"])
            return DocumentInDB(**document_doc)
        return None

    async def get_user_documents(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        status_filter: Optional[DocumentStatus] = None
    ) -> List[DocumentInDB]:
        db = await self.get_database()
        query = {"user_id": user_id}
        if status_filter:
            query["status"] = status_filter
        
        cursor = db.documents.find(query).sort("created_at", -1).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        for document in documents:
            document["_id"] = str(document["_id"])
        
        return [DocumentInDB(**document) for document in documents]

    async def update_document(self, document_id: str, document_update: DocumentUpdate, user_id: str) -> Optional[DocumentInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in document_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.documents.update_one(
            {"_id": document_id, "user_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_document_by_id(document_id, user_id)
        return None

    async def delete_document(self, document_id: str, user_id: str) -> bool:
        db = await self.get_database()
        
        document = await self.get_document_by_id(document_id, user_id)
        if not document:
            return False
        
        await embedding_manager.delete_document(document_id)
        
        file_path = os.path.join(settings.upload_directory, document.file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        result = await db.documents.delete_one({"_id": document_id, "user_id": user_id})
        return result.deleted_count > 0

    async def process_document(self, document_id: str):
        try:
            db = await self.get_database()
            document = await db.documents.find_one({"_id": document_id})
            
            if not document:
                logger.error(f"Document {document_id} not found")
                return
            
            await db.documents.update_one(
                {"_id": document_id},
                {"": {"status": DocumentStatus.PROCESSING}}
            )
            
            file_path = os.path.join(settings.upload_directory, document.file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            text = await self.document_processor.extract_text(file_path, document.file_type)
            text = self.document_processor.clean_text(text)
            
            chunks = self.document_processor.chunk_text(text)
            
            if not chunks:
                raise ValueError("No chunks generated from document")
            
            chunk_ids = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{document_id}_chunk_{i}"
                chunk_ids.append(chunk_id)
            
            metadatas = [
                {
                    "document_id": document_id,
                    "user_id": document["user_id"],
                    "chunk_index": i,
                    "title": document["title"],
                    "subject": document.get("subject"),
                }
                for i in range(len(chunks))
            ]
            
            await embedding_manager.add_documents(
                texts=chunks,
                metadatas=metadatas,
                ids=chunk_ids,
            )
            
            await db.documents.update_one(
                {"_id": document_id},
                {
                    "": {
                        "status": DocumentStatus.COMPLETED,
                        "text_content": text,
                        "chunk_count": len(chunks),
                        "processed_at": datetime.utcnow(),
                    }
                }
            )
            
            logger.info(f"Document {document_id} processed successfully with {len(chunks)} chunks")
        except Exception as e:
            logger.error(f"Document processing failed for {document_id}: {e}")
            await db.documents.update_one(
                {"_id": document_id},
                {
                    "": {
                        "status": DocumentStatus.FAILED,
                        "error_message": str(e),
                    }
                }
            )
            raise
