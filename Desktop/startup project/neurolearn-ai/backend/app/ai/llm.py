from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_community.llms import HuggingFacePipeline
from app.config import settings
from loguru import logger
from typing import Optional


class LLMManager:
    def __init__(self):
        self.llm = None
        self._initialize_llm()

    def _initialize_llm(self):
        try:
            if settings.llm_provider == "ollama":
                logger.info(f"Initializing Ollama LLM: {settings.llm_model}")
                self.llm = ChatOllama(
                    model=settings.llm_model,
                    base_url=settings.ollama_base_url,
                    temperature=settings.llm_temperature,
                    num_predict=settings.llm_max_tokens,
                )
            elif settings.llm_provider == "openai":
                if not settings.openai_api_key:
                    raise ValueError("OpenAI API key not configured")
                logger.info(f"Initializing OpenAI LLM: {settings.llm_model}")
                self.llm = ChatOpenAI(
                    model=settings.llm_model,
                    temperature=settings.llm_temperature,
                    max_tokens=settings.llm_max_tokens,
                    api_key=settings.openai_api_key,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
            
            logger.info("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def get_llm(self):
        if not self.llm:
            self._initialize_llm()
        return self.llm

    def get_streaming_llm(self):
        if not self.llm:
            self._initialize_llm()
        return self.llm


llm_manager = LLMManager()
