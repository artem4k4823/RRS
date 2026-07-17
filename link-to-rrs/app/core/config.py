from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
    )
    DATABASE_URL: str
    RABBIT_URL: str


settings = Settings()