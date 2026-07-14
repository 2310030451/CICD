from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chromadb.config import Settings as ChromaSettings
from app.config import settings
from loguru import logger
from typing import List, Optional
import os


class EmbeddingManager:
    def __init__(self):
        self.embedding_model = None
        self.chroma_client = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of embeddings and ChromaDB"""
        if self._initialized:
            return
        
        try:
            self._initialize_embeddings()
            self._initialize_chroma()
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize embedding manager: {e}")
            raise

    def _initialize_embeddings(self):
        try:
            logger.info(f"Initializing embedding model: {settings.embedding_model}")
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=settings.embedding_model,
                model_kwargs={"device": settings.embedding_device},
                encode_kwargs={"normalize_embeddings": True},
            )
            logger.info("Embedding model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise

    def _initialize_chroma(self):
        try:
            os.makedirs(settings.chroma_persist_directory, exist_ok=True)
            
            logger.info(f"Initializing ChromaDB at {settings.chroma_persist_directory}")
            self.chroma_client = Chroma(
                collection_name=settings.chroma_collection_name,
                embedding_function=self.embedding_model,
                persist_directory=settings.chroma_persist_directory,
                client_settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                ),
            )
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def get_embedding_function(self):
        return self.embedding_model

    def get_chroma_client(self):
        return self.chroma_client

    async def add_documents(
        self,
        texts: List[str],
        metadatas: List[dict],
        ids: List[str],
    ):
        try:
            self._ensure_initialized()
            self.chroma_client.add_texts(texts=texts, metadatas=metadatas, ids=ids)
            logger.info(f"Added {len(texts)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {e}")
            raise

    async def search_documents(
        self,
        query: str,
        user_id: str,
        k: int = 5,
        filter_dict: Optional[dict] = None,
    ) -> List[dict]:
        try:
            self._ensure_initialized()
            filter_dict = filter_dict or {"user_id": user_id}
            
            results = self.chroma_client.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict,
            )
            
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score,
                })
            
            logger.info(f"Found {len(documents)} documents for query")
            return documents
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            raise

    async def delete_user_documents(self, user_id: str):
        try:
            self._ensure_initialized()
            self.chroma_client.delete(where={"user_id": user_id})
            logger.info(f"Deleted all documents for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to delete user documents: {e}")
            raise

    async def delete_document(self, document_id: str):
        try:
            self._ensure_initialized()
            self.chroma_client.delete(where={"document_id": document_id})
            logger.info(f"Deleted document {document_id}")
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            raise


embedding_manager = EmbeddingManager()
