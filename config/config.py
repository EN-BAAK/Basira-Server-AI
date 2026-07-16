from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    ENV: str = "development"
    PORT: int = 8000
    HOST: str = "localhost"
    VERSION: str = "1.0.0"
    
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str
    GEMINI_MODEL: str = "gemini-3.5-flash"
    
    CHROMA_DB_PATH: str = "./chroma_db"

    SERVER_SIDE: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()