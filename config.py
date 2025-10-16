from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    llm_provider: str = "google"
    llm_model: str = "models/gemini-2.0-flash"
    
    # Embedding Configuration
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Document Processing
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_file_size_mb: int = 10
    
    # Retrieval Configuration
    top_k_results: int = 5
    similarity_threshold: float = 0.0
    
    # Storage Paths
    upload_dir: str = "uploaded_documents"
    chroma_db_dir: str = "chroma_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
