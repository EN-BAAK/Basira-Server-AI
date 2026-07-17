from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    ENV: str = "development"
    PORT: int = 8000
    HOST: str = "localhost"
    VERSION: str = "1.0.0"
    
    GHAYMAH_API_KEY: str
    GHAYMAH_BASE_URL: str
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str
    GEMINI_MODEL: str = "gemini-3.5-flash"

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    EMBEDDING_MODEL:str
    
    CHROMA_DB_PATH: str = "./chroma_db"

    SERVER_SIDE: str

    MAX_TOKENS:int = 150

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

class Models:
    QweQ = "QwQ-32B"
    DeepSeek = "DeepSeek-V3-0324"
    gamma = "Gamma-3-4b-it"
    Qwen3 = "Qwen3-32B"

models = Models()

client=  OpenAI(
        api_key=settings.GHAYMAH_API_KEY,
        base_url=settings.GHAYMAH_BASE_URL
    )