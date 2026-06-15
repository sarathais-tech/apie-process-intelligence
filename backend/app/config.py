from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://apie:apie@127.0.0.1:55432/apie"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    ollama_base_url: str = "http://localhost:11434"
    ollama_default_model: str = "llama3"
    ollama_timeout_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
