from app.ai.llm import llm_manager
from app.ai.embeddings import embedding_manager
from app.config import settings
from loguru import logger
from typing import List, Optional, AsyncGenerator, Dict, Any


class RAGPipeline:
    def __init__(self):
        self._initialized = False
        self.llm = None
        self.chroma_client = None
        self.prompt_template = None

    def _ensure_initialized(self):
        """Lazy initialization to avoid startup errors"""
        if self._initialized:
            return
        
        try:
            self.llm = llm_manager.get_llm()
            embedding_manager._ensure_initialized()
            self.chroma_client = embedding_manager.get_chroma_client()
            self._setup_prompt_template()
            self._initialized = True
            logger.info("RAG Pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {e}")
            self._initialized = False

    def _setup_prompt_template(self):
        try:
            from langchain.prompts import PromptTemplate
            self.prompt_template = PromptTemplate(
                template="""You are an AI Tutor for NeuroLearn AI. Your role is to help students learn by answering questions based ONLY on the provided context documents.

Context:
{context}

Conversation History:
{chat_history}

Question: {question}

Instructions:
- Answer the question using ONLY the information from the provided context documents
- If the answer is not available in the context, respond with "I don't have enough information in the provided documents to answer this question."
- Cite the specific documents and sections you used in your answer
- Be clear, concise, and educational
- If you're unsure, admit it rather than making up information
- Format your response in a way that's easy to read and understand

Answer:""",
                input_variables=["context", "chat_history", "question"],
            )
        except Exception as e:
            logger.error(f"Failed to setup prompt template: {e}")
            raise

    async def create_retrieval_chain(
        self,
        user_id: str,
        document_ids: Optional[List[str]] = None,
    ):
        try:
            self._ensure_initialized()
            
            filter_dict = {"user_id": user_id}
            if document_ids:
                filter_dict["document_id"] = {"$in": document_ids}

            retriever = self.chroma_client.as_retriever(
                search_kwargs={
                    "k": 5,
                    "filter": filter_dict,
                }
            )

            # Try to use newer LangChain API, fall back to older if needed
            try:
                from langchain.chains import ConversationalRetrievalChain
                from langchain.memory import ConversationBufferMemory
                
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True,
                    output_key="answer",
                )

                chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    memory=memory,
                    combine_docs_chain_kwargs={"prompt": self.prompt_template},
                    return_source_documents=True,
                    verbose=settings.debug,
                )
                return chain
            except ImportError:
                # Fallback to simpler implementation if newer API not available
                logger.warning("Using simplified RAG implementation due to LangChain version")
                return self._create_simple_chain(retriever, user_id)
                
        except Exception as e:
            logger.error(f"Failed to create retrieval chain: {e}")
            raise

    def _create_simple_chain(self, retriever, user_id: str):
        """Simple fallback chain implementation"""
        class SimpleChain:
            def __init__(self, retriever, llm, prompt_template):
                self.retriever = retriever
                self.llm = llm
                self.prompt_template = prompt_template
                
            async def ainvoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
                question = inputs.get("question", "")
                docs = await self.retriever.ainvoke(question)
                context = "\n\n".join([doc.page_content for doc in docs])
                
                prompt = self.prompt_template.format(
                    context=context,
                    chat_history=inputs.get("chat_history", ""),
                    question=question
                )
                
                response = await self.llm.ainvoke(prompt)
                
                return {
                    "answer": response.content if hasattr(response, 'content') else str(response),
                    "source_documents": docs,
                    "chat_history": inputs.get("chat_history", []),
                }
                
            async def astream(self, inputs: Dict[str, Any]):
                # Simple streaming fallback
                result = await self.ainvoke(inputs)
                yield {"answer": result["answer"]}
        
        return SimpleChain(retriever, self.llm, self.prompt_template)

    async def query(
        self,
        question: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
    ) -> dict:
        try:
            self._ensure_initialized()
            chain = await self.create_retrieval_chain(user_id, document_ids)
            
            response = await chain.ainvoke({"question": question})
            
            sources = []
            if "source_documents" in response:
                for doc in response["source_documents"]:
                    sources.append({
                        "content": doc.page_content[:200],
                        "metadata": doc.metadata,
                        "score": getattr(doc, "score", 0),
                    })

            return {
                "answer": response["answer"],
                "sources": sources,
                "chat_history": response.get("chat_history", []),
            }
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    async def query_stream(
        self,
        question: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
    ) -> AsyncGenerator[str, None]:
        try:
            self._ensure_initialized()
            chain = await self.create_retrieval_chain(user_id, document_ids)
            
            async for chunk in chain.astream({"question": question}):
                if "answer" in chunk:
                    yield chunk["answer"]
        except Exception as e:
            logger.error(f"Streaming query failed: {e}")
            raise


rag_pipeline = RAGPipeline()
