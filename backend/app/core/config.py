"""
Application configuration — loads from environment variables with validation.
Uses pydantic-settings for type-safe config management.
"""

from functools import lru_cache
from typing import Any, List, Literal

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ─────────────────────────────────────────────────
    APP_NAME: str = "AKM45 Vector AI"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # ── Security ─────────────────────────────────────────────
    SECRET_KEY: str = Field(
        default="dev-secret-key-akm45-vector-ai-at-least-32-chars-long-secret",
        min_length=32,
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12

    # ── Database ─────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./local_dev.db"
    )

    # ── Redis ────────────────────────────────────────────────
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0"
    )
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    # ── CORS ─────────────────────────────────────────────────
    ALLOWED_ORIGINS: Any = ["http://localhost:3000", "http://127.0.0.1:3000"]
    TRUSTED_HOSTS: Any = ["*"]

    @field_validator("ALLOWED_ORIGINS", "TRUSTED_HOSTS", "ALLOWED_FILE_TYPES", mode="before")
    @classmethod
    def parse_list_fields(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            v_str = v.strip()
            if v_str.startswith("[") and v_str.endswith("]"):
                import json
                try:
                    return json.loads(v_str)
                except Exception:
                    pass
            return [item.strip().lower() for item in v_str.split(",") if item.strip()]
        return v

    # ── Email ────────────────────────────────────────────────
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@hiresmart.ai"
    EMAIL_FROM_NAME: str = "AKM45 Vector AI"

    # ── File Storage ─────────────────────────────────────────
    STORAGE_BACKEND: Literal["local", "supabase"] = "local"
    UPLOAD_DIR: str = "/app/uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: Any = ["pdf", "docx"]

    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    # ── Ollama / LLM ─────────────────────────────────────────
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_TIMEOUT: int = 120

    # ── Embeddings ───────────────────────────────────────────
    HF_EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    HF_CACHE_DIR: str = "/app/.cache/huggingface"

    # ── FAISS ────────────────────────────────────────────────
    FAISS_INDEX_PATH: str = "/app/data/faiss_index"

    # ── Rate Limiting ─────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60

    def model_post_init(self, __context) -> None:
        """Set derived values after initialization."""
        if not self.CELERY_BROKER_URL:
            object.__setattr__(self, "CELERY_BROKER_URL", self.REDIS_URL)
        if not self.CELERY_RESULT_BACKEND:
            # Use a different Redis DB for results
            object.__setattr__(
                self,
                "CELERY_RESULT_BACKEND",
                self.REDIS_URL.replace("/0", "/1") if self.REDIS_URL.endswith("/0") else self.REDIS_URL + "1",
            )


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — call once, reuse everywhere."""
    return Settings()


settings = get_settings()
