from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "NeuroLearn AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "neurolearn"

    redis_url: str = "redis://localhost:6379/0"

    firebase_project_id: str = ""
    firebase_private_key_id: str = ""
    firebase_private_key: str = ""
    firebase_client_email: str = ""
    firebase_client_id: str = ""
    firebase_auth_uri: str = "https://auth.firebase.com"
    firebase_token_uri: str = "https://oauth2.googleapis.com/token"
    firebase_auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    firebase_client_x509_cert_url: str = "https://www.googleapis.com/robot/v1/metadata/x509/"

    jwt_secret_key: str = "your_jwt_secret_key_change_this_in_production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_rotation: str = "10 MB"
    log_retention: str = "30 days"

    llm_provider: str = "ollama"
    llm_model: str = "llama3"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048
    ollama_base_url: str = "http://localhost:11434"
    openai_api_key: str = ""

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cpu"
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "neurolearn"

    max_file_size: int = 52428800
    allowed_file_types: str = "pdf,docx,pptx,txt,md"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    ocr_enabled: bool = True
    tesseract_cmd: str = "tesseract"

    upload_directory: str = "./uploads"
    processed_directory: str = "./processed"

    enable_gpu: bool = True
    cnn_model: str = "efficientnet_b0"
    ocr_engine: str = "paddleocr"
    image_max_size: int = 10485760
    allowed_image_types: str = "jpg,jpeg,png,bmp,tiff,webp"
    ocr_confidence_threshold: float = 0.5
    cnn_confidence_threshold: float = 0.7

    lstm_model_enabled: bool = True
    lstm_sequence_length: int = 30
    lstm_prediction_horizon: int = 7
    retrain_interval_days: int = 7
    min_training_samples: int = 100

    agent_memory_encryption: bool = True
    agent_max_memory_tokens: int = 10000
    agent_timeout_seconds: int = 30
    enable_agent_orchestration: bool = True

    recommendation_engine_enabled: bool = True
    recommendation_cache_ttl: int = 3600
    min_recommendation_score: float = 0.5

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
