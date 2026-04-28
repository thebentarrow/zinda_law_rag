from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # OpenAI
    openai_api_key: str

    # Chat LLM
    chat_model: str = "gpt-4o-mini"
    chat_temperature: float = 0.2
    chat_max_tokens: int = 1024

    # Embeddings
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # RAG — number of chunks/FAQs returned from ChromaDB and passed to the synthesis LLM
    retrieval_top_k: int = 2

    # Storage
    sqlite_path: str = "/data/app.db"
    chroma_path: str = "/data/chroma"

    # App
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://localhost:80"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()
